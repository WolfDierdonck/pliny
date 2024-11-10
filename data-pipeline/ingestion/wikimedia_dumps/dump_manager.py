import os
import requests

from common.dates import Date

#TODO: use future to pre-fetch next month's worth of data when returning current month's data
class DumpManager:
    def __init__(self, dump_dir):
        self.dump_dir = dump_dir

    def get_page_view_dump_filename(self, date: Date) -> str:
        print("downloading page view dump for date", date)
        response = requests.get(f"https://dumps.wikimedia.org/other/pageview_complete/{date.year}/{date.year}-{date.month:02}/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2")
        os.makedirs("dumps", exist_ok=True)
        with open(f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2", "wb") as file:
            file.write(response.content)
        os.system(f"bzip2 -d dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2")
        return f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user"

    def get_page_revision_dump_filename(self, date: Date) -> str:
        # https://dumps.wikimedia.org/other/mediawiki_history/2024-10/enwiki/2024-10.enwiki.2024-11.tsv.bz2
        print("downloading page revision dump for date", date)
        response = requests.get(f"https://dumps.wikimedia.org/other/mediawiki_history/2024-10/enwiki/2024-10.enwiki.{date.year}-{date.month:02}.tsv.bz2")
        os.makedirs("dumps", exist_ok=True)
        with open(f"dumps/2024-10.enwiki.{date.year}-{date.month:02}.tsv.bz2", "wb") as file:
            file.write(response.content)
        os.system(f"bzip2 -d dumps/2024-10.enwiki.{date.year}-{date.month:02}.tsv.bz2")
        return f"dumps/2024-10.enwiki.{date.year}-{date.month:02}.tsv"

