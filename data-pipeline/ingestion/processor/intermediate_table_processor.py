import concurrent.futures
from common.dates import Date
from sql.wikipedia_data_accessor import WikipediaDataAccessor
from sql.intermediate_table_data import IntermediateTableRow
from ingestion.data_sources.page_revision_data_source import PageRevisionDataSource
from ingestion.data_sources.page_view_data_source import PageViewDataSource


class IntermediateTableProcessor:
    def __init__(
        self,
        revision_data_source: PageRevisionDataSource,
        view_data_source: PageViewDataSource,
        wikipedia_data_accessor: WikipediaDataAccessor,
    ) -> None:
        self.wikipediaDataAccessor = wikipedia_data_accessor
        self.revision_data_source = revision_data_source
        self.view_data_source = view_data_source

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

        for view_future in concurrent.futures.as_completed(view_futures.values()):
            try:
                page = next(
                    page for page, f in view_futures.items() if f == view_future
                )
                views = view_future.result()
                data[page].view_count = views
            except Exception as e:
                print(f"Error processing view future for page {page}: {e}")

        for revision_future in concurrent.futures.as_completed(
            revision_futures.values()
        ):
            try:
                # Retrieve the input (page) from the dictionary
                page = next(
                    page for page, f in revision_futures.items() if f == revision_future
                )
                revision_metadata = revision_future.result()
                data[page].revision_count = revision_metadata.revision_count
                data[page].editor_count = revision_metadata.editor_count
                data[page].revert_count = revision_metadata.revert_count
                data[page].net_bytes_change = revision_metadata.net_bytes_change
            except Exception as e:
                print(f"Error processing revision future for page {page}: {e}")
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
                }
            )

        self.wikipediaDataAccessor.write_to_table(table, rows, True)
