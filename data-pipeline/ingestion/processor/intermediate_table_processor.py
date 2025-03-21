from common.dates import Date
from sql.wikipedia_data_accessor import WikipediaDataAccessor
from sql.intermediate_table_data import IntermediateTableRow
from ingestion.data_sources.page_revision_data_source import PageRevisionDataSource
from ingestion.data_sources.page_view_data_source import PageViewDataSource
from logger import Logger, Component

BAD_PAGE_NAMES = set(
    [
        "Main_Page",
        "Special:Search",
        "Wikipedia:Featured_pictures",
        "Administrators'_noticeboard/Incidents",
        "Sandbox",
        "Teahouse",
        "Help_desk",
        "Portal:Current_events",
        "Administrator_intervention_against_vandalism",
        "Main_Page/Errors",
        "Wikipedia:Teahouse",
        "Wikipedia_talk:Teahouse",
        "Wikipedia_talk:WikiProject_Spam",
        "Wikipedia:Sandbox",
        "Wikipedia:Administrator_intervention_against_vandalism",
        "Wikipedia:Administrator_intervention_against_vandalism/TB2",
        "Wikipedia:Requests_for_page_protection/Increase",
        "Wikipedia:Administrators'_noticeboard/Incidents",
        "Template:Infobox_election/doc",
    ]
)


class IntermediateTableProcessor:
    def __init__(
        self,
        logger: Logger,
        revision_data_source: PageRevisionDataSource,
        view_data_source: PageViewDataSource,
        wikipedia_data_accessor: WikipediaDataAccessor,
    ) -> None:
        self.wikipediaDataAccessor = wikipedia_data_accessor
        self.revision_data_source = revision_data_source
        self.view_data_source = view_data_source
        self.logger = logger

    def process(self, pages: list[str], date: Date) -> None:
        # We need the last week of data to calculate the score
        view_futures = {
            page: self.view_data_source.get_page_views(page, date) for page in pages
        }
        revision_futures = {
            page: self.revision_data_source.get_page_revision_metadata(page, date)
            for page in pages
        }

        data: dict[str, IntermediateTableRow] = {
            page: IntermediateTableRow(page) for page in pages
        }

        for page, view_future in view_futures.items():
            try:
                views = view_future.result()
                data[page].view_count = views
            except Exception as e:
                self.logger.error(
                    f"Error processing view future for page {page}: {e}", Component.CORE
                )

        for page, revision_future in revision_futures.items():
            try:
                revision_metadata = revision_future.result()
                data[page].edit_count = revision_metadata.edit_count
                data[page].editor_count = revision_metadata.editor_count
                data[page].revert_count = revision_metadata.revert_count
                data[page].net_bytes_changed = revision_metadata.net_bytes_changed
                data[page].abs_bytes_changed = revision_metadata.abs_bytes_changed
                data[page].abs_bytes_reverted = revision_metadata.abs_bytes_reverted
            except Exception as e:
                self.logger.error(
                    f"Error processing revision future for page {page}: {e}",
                    Component.CORE,
                )
        table = self.wikipediaDataAccessor.get_table("intermediate_table")

        rows = []
        for page_name, intermediate_table_row in data.items():
            if (
                page_name in BAD_PAGE_NAMES
                or intermediate_table_row.view_count is None
                or intermediate_table_row.view_count < 10
                or page_name.startswith("Wikipedia:")
                or page_name.startswith("Wikipedia_talk:")
                or page_name.startswith("Help:")
            ):
                continue

            rows.append(
                {
                    "date": date.to_py_date().isoformat(),
                    "page_name": page_name,
                    "view_count": intermediate_table_row.view_count,
                    "edit_count": intermediate_table_row.edit_count,
                    "editor_count": intermediate_table_row.editor_count,
                    "revert_count": intermediate_table_row.revert_count,
                    "net_bytes_changed": intermediate_table_row.net_bytes_changed,
                    "abs_bytes_changed": intermediate_table_row.abs_bytes_changed,
                    "abs_bytes_reverted": intermediate_table_row.abs_bytes_reverted,
                }
            )

        self.wikipediaDataAccessor.write_to_table(table, rows, True)
