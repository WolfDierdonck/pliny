import os
from abc import ABC, abstractmethod
from concurrent.futures import Future

import requests

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

class PageViewDummy(PageViewDataSource):
    def get_page_views(self, page: str, date: Date) -> Future[int]:
        future: Future[int] = Future()
        future.set_result(0)
        return future


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

class PageViewDumpFile(PageViewDataSource):
    def __init__(self, dump_dir: str) -> None:
        # maps month/year to a dump file's table
        # dump file table maps (page, date) to view count
        self.dump_dir = dump_dir
        self.dump_files: dict[Date, dict[tuple[str, Date], int]] = {}
        # unsure about what the last column actually represents, doesn't seem to specify in docs
        #['en.wikipedia', '!', '7712754', 'desktop', '21', 'B1C1D2E1F1G1J4K1L3N1O1Q1U1V1X1\n']
        cols_names = "wiki_code,page_title,page_id,access_method,page_views,agent_identifier"
        self.col_name_to_index = {col: i for i, col in enumerate(cols_names.split(","))}
        super().__init__()

    def load_dump_file(self, date: Date) -> dict[tuple[str, Date], int]:
        # load the dump file into memory
        # pageviews-20241101-user  
        filename = os.path.expanduser(f"{self.dump_dir}/pageviews-{date.year}{date.month:02}{date.day:02}-user")

        #TODO: make this async, pre-downlad the file
        if(not os.path.exists(filename)):
                print("downloading page view dump for date", date)
                # https://dumps.wikimedia.org/other/pageview_complete/2024/2024-11/pageviews-20241101-user.bz2
                response = requests.get(f"https://dumps.wikimedia.org/other/pageview_complete/{date.year}/{date.year}-{date.month:02}/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2")
                os.makedirs(self.dump_dir, exist_ok=True)
                with open(f"{self.dump_dir}/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2", "wb") as file:
                    file.write(response.content)
                os.system(f"bzip2 -d {self.dump_dir}/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2")
        
        # read the file and parse as stream
        # open the absolute path to the file
        out: dict[tuple[str, Date], int] = {}
        with open(filename, "r") as f:  
            for line in f:
                cols = line.split(" ")
                # skip non-enwiki
                if cols[self.col_name_to_index["wiki_code"]] != "en.wikipedia":
                    continue
                
                page = cols[self.col_name_to_index["page_title"]]
                if (page,date) not in out:
                    out[(page, date)] = 0
                
                out[(page, date)] += int(cols[self.col_name_to_index["page_views"]])

        return out

    def get_page_views(
        self, page: str, date: Date
    ) -> Future[int]:
        # first, load the correct dump file into memory
        dump_file = self.dump_files.get(date)
        if dump_file is None:
            dump_file = self.load_dump_file(date)
            self.dump_files[date] = dump_file

        # then, get the metadata for the page/date
        # return a future that is already done

        future: Future[int] = Future()
        res = dump_file.get((page, date))
        future.set_result(0 if res is None else res)
        return future
        