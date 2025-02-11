from concurrent.futures import Future
import concurrent.futures
import os
import requests
from tqdm import tqdm
from datetime import datetime, timedelta

from common.dates import Date, DateRange
from logger import Logger, Component


class DumpManager:
    def __init__(self, logger: Logger, dump_dir: str, date_range: DateRange) -> None:
        self.logger = logger
        self.dump_dir = dump_dir
        self.date_range = date_range
        self.dumps_downloaded: dict[Date, Future[str]] = {}
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)

    def _download_with_progress_bar(
        self, url: str, fname: str, chunk_size: int = 1024 * 10
    ) -> None:
        resp = requests.get(url, stream=True)
        total = int(resp.headers.get("content-length", 0))
        with open(fname, "wb") as file, tqdm(
            desc=fname,
            total=total,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=chunk_size):
                size = file.write(data)
                bar.update(size)

    def download_page_view_dump(self, date: Date) -> Future[str]:
        def download_page(date: Date) -> str:
            # check if file exists
            if os.path.exists(
                f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user"
            ):
                return f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user"

            os.makedirs("dumps", exist_ok=True)

            self.logger.info(
                f"Downloading page view dump for date {date}", Component.DATASOURCE
            )
            url = f"https://dumps.wikimedia.org/other/pageview_complete/{date.year}/{date.year}-{date.month:02}/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2"
            filename = (
                f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2"
            )
            self._download_with_progress_bar(url, filename)

            self.logger.info(
                f"Decompressing page view dump for date {date}", Component.DATASOURCE
            )
            os.system(
                f"bzip2 -d dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2"
            )

            # pre-fetch next day's data, self-recursive
            next_day = date.add_days(1)
            if (
                next_day <= self.date_range.end
                and next_day not in self.dumps_downloaded
            ):
                self.dumps_downloaded[next_day] = self.executor.submit(
                    download_page, next_day
                )
            return f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user"

        return self.executor.submit(download_page, date)

    def get_page_view_dump_filename(self, date: Date) -> str:
        if date not in self.dumps_downloaded:
            # typically this doesn't run, only if out of sequence
            self.dumps_downloaded[date] = self.download_page_view_dump(date)
        return self.dumps_downloaded[date].result()

    def get_page_revision_dump_filename(self, date: Date) -> str:
        # check if file exists

        # get the current month
        current_date = datetime.now()
        current_date = current_date.replace(month=1)

        if date.year == current_date.year and date.month == current_date.month:
            raise ValueError("Cannot download current month's data")

        last_month_date = current_date.replace(day=1) - timedelta(days=1)

        last_month_year = last_month_date.year
        last_month_month = last_month_date.month

        final_file_name = f"{last_month_year}-{last_month_month:02}.enwiki.{date.year}-{date.month:02}.tsv"
        final_file_path = f"dumps/{final_file_name}"

        if os.path.exists(final_file_path):
            return final_file_path

        self.logger.info(
            f"Downloading page revision dump for date {date}", Component.DATASOURCE
        )
        # https://dumps.wikimedia.org/other/mediawiki_history/2024-10/enwiki/2024-10.enwiki.2024-11.tsv.bz2
        intermediate_file_name = final_file_name + ".bz2"

        url = f"https://dumps.wikimedia.org/other/mediawiki_history/{last_month_year}-{last_month_month:02}/enwiki/{intermediate_file_name}"
        self._download_with_progress_bar(url, f"dumps/{intermediate_file_name}")

        self.logger.info(
            f"Decompressing page revision dump for date {date}", Component.DATASOURCE
        )
        os.system(f"bzip2 -d dumps/{intermediate_file_name}")
        return final_file_path

    def delete_page_view_dump(self, date: Date) -> None:
        filename = self.get_page_view_dump_filename(date)
        os.remove(filename)

    def delete_page_revision_dump(self, date: Date) -> None:
        filename = self.get_page_revision_dump_filename(date)
        os.remove(filename)
