import os
import requests
from common.dates import Date

def load_dump(date: Date) -> None:
    print("downloading page view dump for date", date)
    # https://dumps.wikimedia.org/other/pageview_complete/2024/2024-11/pageviews-20241101-user.bz2
    response = requests.get(f"https://dumps.wikimedia.org/other/pageview_complete/{date.year}/{date.year}-{date.month:02}/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2")
    os.makedirs("dumps", exist_ok=True)
    with open(f"dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2", "wb") as file:
        file.write(response.content)
    os.system(f"bzip2 -d dumps/pageviews-{date.year}{date.month:02}{date.day:02}-user.bz2")

load_dump(Date(2024, 11, 1))
