from abc import ABC, abstractmethod
from concurrent.futures import Future
from io import TextIOWrapper

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


class PageRevisionMonthlyDumpFile(PageRevisionDataSource):
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
        self.dates_data: dict[Date, dict[str, PageRevisionMetadata]] = {}
        self.logger = logger
        self.dump_manager = dump_manager
        cols_names = "wiki_db	event_entity	event_type	event_timestamp	event_comment	event_user_id	event_user_text_historical	event_user_text	event_user_blocks_historical	event_user_blocks	event_user_groups_historical	event_user_groups	event_user_is_bot_by_historical	event_user_is_bot_by	event_user_is_created_by_self	event_user_is_created_by_system	event_user_is_created_by_peer	event_user_is_anonymous	event_user_registration_timestamp	event_user_creation_timestamp	event_user_first_edit_timestamp	event_user_revision_count	event_user_seconds_since_previous_revision	page_id	page_title_historical	page_title	page_namespace_historical	page_namespace_is_content_historical	page_namespace	page_namespace_is_content	page_is_redirect	page_is_deleted	page_creation_timestamp	page_first_edit_timestamp	page_revision_count	page_seconds_since_previous_revision	user_id	user_text_historical	user_text	user_blocks_historical	user_blocks	user_groups_historical	user_groups	user_is_bot_by_historical	user_is_bot_by	user_is_created_by_self	user_is_created_by_system	user_is_created_by_peer	user_is_anonymous	user_registration_timestamp	user_creation_timestamp	user_first_edit_timestamp	revision_id	revision_parent_id	revision_minor_edit	revision_deleted_parts	revision_deleted_parts_are_suppressed	revision_text_bytes	revision_text_bytes_diff	revision_text_sha1	revision_content_model	revision_content_format	revision_is_deleted_by_page_deletion	revision_deleted_by_page_deletion_timestamp	revision_is_identity_reverted	revision_first_identity_reverting_revision_id	revision_seconds_to_identity_revert	revision_is_identity_revert	revision_is_from_before_page_creation	revision_tags"
        self.col_name_to_index = {
            col: i for i, col in enumerate(cols_names.split("\t"))
        }
        super().__init__()

    def load_dump_file(self, date: Date) -> None:
        def int_or_zero(s: str) -> int:
            return int(
                s if s.isdigit() or (s.startswith("-") and s[1:].isdigit()) else 0
            )

        # load the dump file for the date's month into memory
        # jan 2024 is 2024-10.enwiki.2024-01.tsv
        # (the first 2024-10 is the dump date, the second date is the data date)
        month = Date(date.year, date.month, 1)

        filename = self.dump_manager.get_page_revision_monthly_dump_filename(month)

        aggregated_data: dict[Date, dict[str, list]] = {}
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
                if date not in aggregated_data:
                    aggregated_data[date] = {}

                if page not in aggregated_data[date]:
                    aggregated_data[date][page] = []

                aggregated_data[date][page].append(
                    {
                        # using event_user_text_historical as some revisions are made by editors with no id but a name
                        "event_user_text_historical": cols[
                            self.col_name_to_index["event_user_text_historical"]
                        ],
                        "revision_text_bytes_diff": cols[
                            self.col_name_to_index["revision_text_bytes_diff"]
                        ],
                        "revision_tags": cols[self.col_name_to_index["revision_tags"]],
                    }
                )
        # now that entries are grouped by page/date, we can generate the final metadata
        for date, page_entries in aggregated_data.items():
            for page, entries in page_entries.items():
                if date not in self.dates_data:
                    self.dates_data[date] = {}

                self.dates_data[date][page] = PageRevisionMetadata(
                    edit_count=len(entries),
                    editor_count=len(
                        set(entry["event_user_text_historical"] for entry in entries)
                    ),
                    revert_count=sum(
                        "revert" in entry["revision_tags"] for entry in entries
                    ),
                    net_bytes_changed=sum(
                        int_or_zero(entry["revision_text_bytes_diff"])
                        for entry in entries
                    ),
                    abs_bytes_changed=sum(
                        abs(int_or_zero(entry["revision_text_bytes_diff"]))
                        for entry in entries
                    ),
                    abs_bytes_reverted=sum(
                        abs(int_or_zero(entry["revision_text_bytes_diff"]))
                        for entry in entries
                        if "revert" in entry["revision_tags"]
                    ),
                )

    def get_page_revision_metadata(
        self, page: str, date: Date
    ) -> Future[PageRevisionMetadata]:
        # first, load the correct dump file into memory
        date_data = self.dates_data.get(date)
        if date_data is None:
            self.load_dump_file(date)
            date_data = self.dates_data[date]

        # then, get the metadata for the page/date
        # return a future that is already done

        future: Future[PageRevisionMetadata] = Future()
        res = date_data.get(page)
        future.set_result(
            PageRevisionMetadata(0, 0, 0, 0, 0, 0) if res is None else res
        )
        return future


class PageRevisionDailyDumpFile(PageRevisionDataSource):
    class RevisionEntry:
        def __init__(self):
            self.page_name = ""
            self.editor_name = ""
            self.comment = ""
            self.text_bytes = 0
            self.timestamp = ""

        def __str__(self):
            return f"Page: {self.page_name}, Editor: {self.editor_name}, Comment: {self.comment}, Text bytes: {self.text_bytes}, Timestamp: {self.timestamp}"

        def __repr__(self):
            return self.__str__()

    def __init__(self, logger: Logger, dump_manager: DumpManager) -> None:
        # maps month/year to a dump file's table
        # dump file table maps (page, date) to revision metadata
        self.logger = logger
        self.dump_manager = dump_manager
        self.dump_files: dict[Date, dict[str, PageRevisionMetadata]] = {}
        super().__init__()

    def _process_dump_file(
        self, file_iterator: TextIOWrapper, date: Date
    ) -> dict[str, PageRevisionMetadata]:
        result: dict[str, PageRevisionMetadata] = {}
        while True:
            current_line = ""
            try:
                current_line = next(file_iterator)
            except StopIteration:
                break

            if current_line.startswith("  <page>"):
                PAGE_TITLE = ""
                revision_entries: list[PageRevisionDailyDumpFile.RevisionEntry] = []
                while True:
                    inside_page_line = next(file_iterator)
                    if inside_page_line.startswith("  </page>"):
                        break

                    if inside_page_line.startswith("    <title>"):
                        PAGE_TITLE = (
                            inside_page_line.replace("<title>", "")
                            .replace("</title>", "")
                            .strip()
                            .replace(" ", "_")
                        )

                    if inside_page_line.startswith("    <revision>"):
                        revision_entry = PageRevisionDailyDumpFile.RevisionEntry()
                        revision_entry.page_name = PAGE_TITLE
                        while True:
                            inside_revision_line = next(file_iterator)
                            if inside_revision_line.startswith("    </revision>"):
                                break

                            if inside_revision_line.startswith("      <contributor>"):
                                while True:
                                    inside_contributor_line = next(file_iterator)
                                    if inside_contributor_line.startswith(
                                        "      </contributor>"
                                    ):
                                        break

                                    if inside_contributor_line.startswith(
                                        "        <username>"
                                    ):
                                        revision_entry.editor_name = (
                                            inside_contributor_line.replace(
                                                "<username>", ""
                                            )
                                            .replace("</username>", "")
                                            .strip()
                                        )

                                    if inside_contributor_line.startswith(
                                        "        <ip>"
                                    ):
                                        revision_entry.editor_name = (
                                            inside_contributor_line.replace("<ip>", "")
                                            .replace("</ip>", "")
                                            .strip()
                                        )

                            if inside_revision_line.startswith("      <comment>"):
                                revision_entry.comment = (
                                    inside_revision_line.replace("<comment>", "")
                                    .replace("</comment>", "")
                                    .strip()
                                    .lower()
                                )

                            if inside_revision_line.startswith("      <text"):
                                revision_entry.text_bytes = int(
                                    inside_revision_line.split('bytes="')[1].split('"')[
                                        0
                                    ]
                                )

                            if inside_revision_line.startswith("      <timestamp>"):
                                revision_entry.timestamp = (
                                    inside_revision_line.replace("<timestamp>", "")
                                    .replace("</timestamp>", "")
                                    .strip()
                                )

                        revision_entries.append(revision_entry)

                # Now process the page data
                # We want to filter the revisions to only include those that are from the date
                revision_entries = [
                    revision_entry
                    for revision_entry in revision_entries
                    if revision_entry.timestamp.startswith(
                        f"{date.year}-{date.month:02}-{date.day:02}"
                    )
                ]
                if revision_entries:
                    edit_count = len(revision_entries)
                    editor_count = len(
                        set(
                            revision_entry.editor_name
                            for revision_entry in revision_entries
                        )
                    )
                    revert_count = sum(
                        "revert" in revision_entry.comment
                        for revision_entry in revision_entries
                    )

                    byte_deltas = []
                    for i in range(len(revision_entries) - 1):
                        byte_deltas.append(
                            revision_entries[i + 1].text_bytes
                            - revision_entries[i].text_bytes
                        )

                    net_bytes_changed = sum(byte_deltas)
                    abs_bytes_changed = sum(abs(delta) for delta in byte_deltas)

                    revert_byte_deltas = []
                    for i in range(len(revision_entries) - 1):
                        if "revert" in revision_entries[i + 1].comment:
                            revert_byte_deltas.append(
                                revision_entries[i + 1].text_bytes
                                - revision_entries[i].text_bytes
                            )

                    abs_bytes_reverted = sum(abs(delta) for delta in revert_byte_deltas)

                    metadata = PageRevisionMetadata(
                        edit_count=edit_count,
                        editor_count=editor_count,
                        revert_count=revert_count,
                        net_bytes_changed=net_bytes_changed,
                        abs_bytes_changed=abs_bytes_changed,
                        abs_bytes_reverted=abs_bytes_reverted,
                    )

                    result[PAGE_TITLE] = metadata

        return result

    def load_dump_file(self, date: Date) -> dict[str, PageRevisionMetadata]:
        # To load the data for a date (Jan 24th), we actually need two dump files
        # This is because the dump file for the 24th contains noon 23rd to noon 24th data
        # So we need to load the 24th and the 25th dump files
        next_date = date.add_days(1)
        filename = self.dump_manager.get_page_revision_daily_dump_filename(date)
        next_filename = self.dump_manager.get_page_revision_daily_dump_filename(
            next_date
        )

        self.logger.info(
            f"Parsing revision dump for date: {date}", Component.DATASOURCE
        )
        file_iterator = open(filename, "r", encoding="utf-8")
        current_date_data = self._process_dump_file(file_iterator, date)

        self.logger.info(
            f"Parsing revision dump for date: {next_date}", Component.DATASOURCE
        )
        next_file_iterator = open(next_filename, "r", encoding="utf-8")
        next_date_data = self._process_dump_file(next_file_iterator, date)

        # Now we need to merge the two dictionaries
        final_data: dict[str, PageRevisionMetadata] = {}
        for page, metadata in current_date_data.items():
            final_data[page] = metadata

        for page, metadata in next_date_data.items():
            if page in final_data:
                final_data[page] = PageRevisionMetadata(
                    edit_count=final_data[page].edit_count + metadata.edit_count,
                    editor_count=final_data[page].editor_count + metadata.editor_count,
                    revert_count=final_data[page].revert_count + metadata.revert_count,
                    net_bytes_changed=final_data[page].net_bytes_changed
                    + metadata.net_bytes_changed,
                    abs_bytes_changed=final_data[page].abs_bytes_changed
                    + metadata.abs_bytes_changed,
                    abs_bytes_reverted=final_data[page].abs_bytes_reverted
                    + metadata.abs_bytes_reverted,
                )
            else:
                final_data[page] = metadata

        return final_data

    def get_page_revision_metadata(
        self, page: str, date: Date
    ) -> Future[PageRevisionMetadata]:
        # first, load the correct dump file into memory
        dump_file = self.dump_files.get(date)
        if dump_file is None:
            # clear old dump files, for memory
            self.dump_files = {}
            dump_file = self.load_dump_file(date)
            self.dump_files[date] = dump_file
        # then, get the metadata for the page/date
        # return a future that is already done

        future: Future[PageRevisionMetadata] = Future()
        res = dump_file.get(page)
        future.set_result(
            PageRevisionMetadata(0, 0, 0, 0, 0, 0) if res is None else res
        )
        return future
