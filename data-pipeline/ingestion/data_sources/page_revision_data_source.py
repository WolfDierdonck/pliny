import os
from abc import ABC, abstractmethod
from concurrent.futures import Future

from common.dates import Date
from common.page_revision_metadata import PageRevisionMetadata
from ingestion.mediawiki_api.mediawiki_api import MediaWikiAPI

from ingestion.wikimedia_dumps.dump_manager import DumpManager
from logger import Logger, Component


class PageRevisionDataSource(ABC):
    @abstractmethod
    def get_page_revision_metadata(
        self, page: str, date: Date
    ) -> Future[PageRevisionMetadata]:
        """
        Abstract method to get page revision metadata.

        Args:
            page (str): The page to get revision metadata for.
            date (datetime): The date to get revision metadata for.

        Returns:
            dict: The revision metadata for the page.
        """
        pass


class PageRevisionAPI(PageRevisionDataSource):
    def __init__(self) -> None:
        self.media_wiki_api = MediaWikiAPI()

    def get_page_revision_metadata(
        self, page: str, date: Date
    ) -> Future[PageRevisionMetadata]:
        return self.media_wiki_api.get_page_revision_metadata(page, date)


class PageRevisionDumpFile(PageRevisionDataSource):
    # while the PageRevisionDataSource promises random access to page/date -> metadata
    # due to the nature of the workflow and the dumpfiles
    # we will assume that dates are processed in order and that we can load the dump file into memory
    # so we can process the dumps as fast as we can

    @staticmethod
    def parse_date(date_iso: str) -> Date:
        year, month, day = date_iso.split(" ")[0].split("-")
        return Date(int(year), int(month), int(day))

    def __init__(self, logger: Logger, dump_manager: DumpManager) -> None:
        # maps month/year to a dump file's table
        # dump file table maps (page, date) to revision metadata
        self.dump_files: dict[Date, dict[tuple[str, Date], PageRevisionMetadata]] = {}
        self.logger = logger
        self.dump_manager = dump_manager
        cols_names = "wiki_db	event_entity	event_type	event_timestamp	event_comment	event_user_id	event_user_text_historical	event_user_text	event_user_blocks_historical	event_user_blocks	event_user_groups_historical	event_user_groups	event_user_is_bot_by_historical	event_user_is_bot_by	event_user_is_created_by_self	event_user_is_created_by_system	event_user_is_created_by_peer	event_user_is_anonymous	event_user_registration_timestamp	event_user_creation_timestamp	event_user_first_edit_timestamp	event_user_revision_count	event_user_seconds_since_previous_revision	page_id	page_title_historical	page_title	page_namespace_historical	page_namespace_is_content_historical	page_namespace	page_namespace_is_content	page_is_redirect	page_is_deleted	page_creation_timestamp	page_first_edit_timestamp	page_revision_count	page_seconds_since_previous_revision	user_id	user_text_historical	user_text	user_blocks_historical	user_blocks	user_groups_historical	user_groups	user_is_bot_by_historical	user_is_bot_by	user_is_created_by_self	user_is_created_by_system	user_is_created_by_peer	user_is_anonymous	user_registration_timestamp	user_creation_timestamp	user_first_edit_timestamp	revision_id	revision_parent_id	revision_minor_edit	revision_deleted_parts	revision_deleted_parts_are_suppressed	revision_text_bytes	revision_text_bytes_diff	revision_text_sha1	revision_content_model	revision_content_format	revision_is_deleted_by_page_deletion	revision_deleted_by_page_deletion_timestamp	revision_is_identity_reverted	revision_first_identity_reverting_revision_id	revision_seconds_to_identity_revert	revision_is_identity_revert	revision_is_from_before_page_creation	revision_tags"
        self.col_name_to_index = {
            col: i for i, col in enumerate(cols_names.split("\t"))
        }
        super().__init__()

    def load_dump_file(
        self, date: Date
    ) -> dict[tuple[str, Date], PageRevisionMetadata]:
        # load the dump file into memory
        # jan 2024 is 2024-10.enwiki.2024-01.tsv
        # (the first 2024-10 is the dump date, the second date is the data date)
        filename = self.dump_manager.get_page_revision_dump_filename(date)
        if not os.path.exists(filename):
            self.dump_manager.get_page_revision_dump_filename(date)

        page_date_to_entries: dict[tuple[str, Date], list] = {}
        # read the file and parse as stream
        # open the absolute path to the file
        with open(filename, "r") as f:
            self.logger.info(
                f"Parsing revision dump for month: {date}", Component.DATASOURCE
            )
            for line in f:
                cols = line.split("\t")
                # skip non-revisions
                if cols[self.col_name_to_index["event_entity"]] != "revision":
                    continue
                page = cols[self.col_name_to_index["page_title"]]
                date = self.parse_date(cols[self.col_name_to_index["event_timestamp"]])
                # generate page revision metadata
                if page not in page_date_to_entries:
                    page_date_to_entries[(page, date)] = []
                page_date_to_entries[(page, date)].append(
                    {
                        "event_user_id": cols[self.col_name_to_index["event_user_id"]],
                        "revision_text_bytes": cols[
                            self.col_name_to_index["revision_text_bytes"]
                        ],
                        "revision_tags": cols[self.col_name_to_index["revision_tags"]],
                    }
                )
        # now that entries are grouped by page/date, we can generate the final metadata
        out: dict[tuple[str, Date], PageRevisionMetadata] = {}
        for (page, date), entries in page_date_to_entries.items():
            out[(page, date)] = PageRevisionMetadata(
                revision_count=len(entries),
                editor_count=len(set(entry["event_user_id"] for entry in entries)),
                # net_bytes_change is the sum of all revision_text_bytes, not a total delta
                net_bytes_change=sum(
                    int(
                        entry["revision_text_bytes"]
                        if entry["revision_text_bytes"].isnumeric()
                        else 0
                    )
                    for entry in entries
                ),
                revert_count=sum(
                    "revert" in entry["revision_tags"] for entry in entries
                ),
            )

        # return the dump file as a dict
        return out

    def get_page_revision_metadata(
        self, page: str, date: Date
    ) -> Future[PageRevisionMetadata]:
        # first, load the correct dump file into memory
        dump_file = self.dump_files.get(date)
        if dump_file is None:
            dump_file = self.load_dump_file(date)
            self.dump_files[date] = dump_file

        # then, get the metadata for the page/date
        # return a future that is already done

        future: Future[PageRevisionMetadata] = Future()
        res = dump_file.get((page, date))
        future.set_result(PageRevisionMetadata(0, 0, 0, 0) if res is None else res)
        return future
