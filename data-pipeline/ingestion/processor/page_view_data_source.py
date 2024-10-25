from abc import ABC, abstractmethod
from concurrent.futures import Future

from common.dates import Date, DateRange
from ingestion.analytics_api.analytics_api import AnalyticsAPI
from common.time_series import TimeSeries


class PageViewDataSource(ABC):
    @abstractmethod
    def get_page_views(self, page: str, date: Date) -> Future[int]:
        """
        Abstract method to get page revision metadata.

        Args:
            page (str): The page to get revision metadata for.
            date (datetime): The date to get revision metadata for.

        Returns:
            dict: The revision metadata for the page.
        """
        pass


class PageViewAPI(PageViewDataSource):
    def __init__(self) -> None:
        self.analytics_api = AnalyticsAPI()

    def get_page_views(self, page: str, date: Date) -> Future[int]:
        future = self.analytics_api.get_page_views(page, DateRange(date, date))
        processed_future: Future[int] = Future()

        def callback(fut: Future[tuple[str, DateRange, TimeSeries]]) -> None:
            try:
                result = fut.result()
                _, _, views = result
                processed_future.set_result(int(views.get_data_point(date)))
            except Exception as e:
                fut.set_exception(e)

        future.add_done_callback(callback)
        return processed_future
