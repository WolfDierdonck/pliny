from concurrent.futures import Future
import concurrent.futures
import os
import requests

from common.dates import Date, DateRange

class DumpManager:
    def __init__(self, dump_dir, date_range: DateRange) -> None:
        self.dump_dir = dump_dir
        self.date_range = date_range
        self.dumps_downloaded: dict[Date, Future[str]] = {}
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
        
    def download_page_view_dump(self, date: Date) -> Future[str]:
        def download_page(date: Date) -> str:
            #check if file exists
            if os.path.exists(f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user"):
                return f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user"
            print("downloading page view dump for date", date)
            response = requests.get(f"https://dumps.wikimedia.org/other/pageview_complete/{date.year}/{date.year}-{date.month:02}/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2")
            os.makedirs("dumps", exist_ok=True)
            with open(f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2", "wb") as file:
                file.write(response.content)
            os.system(f"bzip2 -d dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2")

            # pre-fetch next day's data, self-recursive
            next_day = date.add_days(1)
            if next_day <= self.date_range.end and next_day not in self.dumps_downloaded: 
                self.dumps_downloaded[next_day] = self.executor.submit(self.get_page_view_dump_filename, next_day)
            return f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user"
        return self.executor.submit(download_page, date)
        


    def get_page_view_dump_filename(self, date: Date) -> str:
        if date not in self.dumps_downloaded:
            # typically this doesn't run, only if out of sequence
            self.dumps_downloaded[date] = self.download_page_view_dump(date)
        return self.dumps_downloaded[date].result()


    def get_page_revision_dump_filename(self, date: Date) -> str:
        #check if file exists
        if os.path.exists(f"dumps/2024-10.enwiki.{date.year}-{date.month:02}.tsv"):
            return f"dumps/2024-10.enwiki.{date.year}-{date.month:02}.tsv"

        print("downloading page revision dump for date", date)
        # https://dumps.wikimedia.org/other/mediawiki_history/2024-10/enwiki/2024-10.enwiki.2024-11.tsv.bz2
        response = requests.get(f"https://dumps.wikimedia.org/other/mediawiki_history/2024-10/enwiki/2024-10.enwiki.{date.year}-{date.month:02}.tsv.bz2")
        os.makedirs("dumps", exist_ok=True)
        with open(f"dumps/2024-10.enwiki.{date.year}-{date.month:02}.tsv.bz2", "wb") as file:
            file.write(response.content)
        os.system(f"bzip2 -d dumps/2024-10.enwiki.{date.year}-{date.month:02}.tsv.bz2")
        return f"dumps/2024-10.enwiki.{date.year}-{date.month:02}.tsv"

