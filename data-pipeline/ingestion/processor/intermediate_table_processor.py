from common.dates import Date
from sql.wikipedia_data_accessor import WikipediaDataAccessor
from sql.intermediate_table_data import IntermediateTableRow
from ingestion.data_sources.page_revision_data_source import PageRevisionDataSource
from ingestion.data_sources.page_view_data_source import PageViewDataSource
from logger import Logger, Component


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
                data[page].revision_count = revision_metadata.revision_count
                data[page].editor_count = revision_metadata.editor_count
                data[page].revert_count = revision_metadata.revert_count
                data[page].net_bytes_change = revision_metadata.net_bytes_change
                data[page].total_bytes_reverted = revision_metadata.total_bytes_reverted
            except Exception as e:
                self.logger.error(
                    f"Error processing revision future for page {page}: {e}",
                    Component.CORE,
                )
        table = self.wikipediaDataAccessor.get_table("intermediate_table")

        rows = []
        for page_name, intermediate_table_row in data.items():
            rows.append(
                {
                    "date": date.to_py_date().isoformat(),
                    "page_name": page_name,
                    "view_count": intermediate_table_row.view_count,
                    "revision_count": intermediate_table_row.revision_count,
                    "net_bytes_change": intermediate_table_row.net_bytes_change,
                    "editor_count": intermediate_table_row.editor_count,
                    "revert_count": intermediate_table_row.revert_count,
                    "total_bytes_reverted": intermediate_table_row.total_bytes_reverted
                }
            )

        self.wikipediaDataAccessor.write_to_table(table, rows, True)
