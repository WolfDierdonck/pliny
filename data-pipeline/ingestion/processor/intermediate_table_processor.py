import concurrent.futures
from ..analytics_api.analytics_api import AnalyticsAPI
from common.dates import Date, DateRange
from common.dates import Date, DateRange
from sql.wikipedia_data_accessor import WikipediaDataAccessor
from ingestion.mediawiki_api.mediawiki_api import MediaWikiAPI
from sql.intermediate_table_data import IntermediateTableRow


class IntermediateTableProcessor:
    def __init__(self) -> None:
        self.wikipediaDataAccessor = WikipediaDataAccessor(
            "PLINY_BIGQUERY_SERVICE_ACCOUNT"
        )
        self.analytics_api = AnalyticsAPI()
        self.media_wiki_api = MediaWikiAPI()

    def process(self, pages: list[str], date: Date) -> None:
        # We need the last week of data to calculate the score
        date_range = DateRange(date, date)

        # view_futures = [
        #     self.analytics_api.get_page_views(page, date_range) for page in pages
        # ]
        # edit_futures = [
        #     self.analytics_api.get_page_net_bytes_diff(page, date_range)
        #     for page in pages
        # ]
        revision_futures = [
            self.media_wiki_api.get_page_revision_metadata(page, date) for page in pages
        ]

        data: dict[str, IntermediateTableRow] = {
            page: IntermediateTableRow(page) for page in pages
        }

        # for view_future in concurrent.futures.as_completed(view_futures):
        #     try:
        #         page, date_range, views = view_future.result()
        #         data[page].view_count = int(views.get_data_point(date))
        #     except Exception as e:
        #         print(f"Error processing view future: {e}")

        # for edit_future in concurrent.futures.as_completed(edit_futures):
        #     try:
        #         page, date_range, edits = edit_future.result()
        #         data[page].net_bytes_change = int(edits.get_data_point(date))
        #     except Exception as e:
        #         print(f"Error processing edit future: {e}")

        for revision_future in concurrent.futures.as_completed(revision_futures):
            try:
                page, revision_metadata = revision_future.result()
                data[page].revision_count = revision_metadata.revision_count
                data[page].editor_count = revision_metadata.editor_count
                data[page].revert_count = revision_metadata.revert_count
                data[page].net_bytes_change = revision_metadata.net_bytes_change
            except Exception as e:
                print(f"Error processing revision future: {e}")

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
