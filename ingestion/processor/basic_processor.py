import concurrent.futures
from ..analytics_api.analytics_api import AnalyticsAPI
from common.dates import Date, DateRange
from common.pages import PageMetadata
from common.dates import Date, DateRange
from common.pages import PageMetadata


class BasicProcessor:
    def __init__(self) -> None:
        pass

    def process_pages(self, pages, date: Date) -> dict[str, PageMetadata]:
        api = AnalyticsAPI()

        # We need the last week of data to calculate the score
        date_range = DateRange(date.add_days(-7), date)

        view_futures = [api.get_page_views(page, date_range) for page in pages]
        edit_futures = [api.get_page_edits(page, date_range) for page in pages]

        all_futures = {future: "view" for future in view_futures}
        all_futures.update({future: "edit" for future in edit_futures})

        data = {page: PageMetadata(page, date_range) for page in pages}
        for future in concurrent.futures.as_completed(all_futures):
            future_type = all_futures[future]
            try:
                if future_type == "view":
                    page, date_range, views = future.result()
                    data[page].views = views
                elif future_type == "edit":
                    page, date_range, edits = future.result()
                    data[page].net_bytes_difference = edits

            except Exception as e:
                print(f"Error processing {future_type} future: {e}")

        return data
