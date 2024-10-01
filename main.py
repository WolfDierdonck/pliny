import concurrent.futures
from analytics_api.analytics_api import AnalyticsAPI
from dotenv import load_dotenv
from common.dates import Date, DateRange
from processor.basic_processor import BasicProcessor

load_dotenv(dotenv_path=".env")

api = AnalyticsAPI()
date_range = DateRange(
    Date(day=1, month=7, year=2024), Date(day=10, month=7, year=2024)
)

pages_to_process = [
    "Earth",
    "Moon",
    "Sun",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
]


days_to_index: dict[Date, int] = {}
i = 0
for date in date_range:
    days_to_index[date] = i
    i += 1

futures = [
    api.get_page_views(page, DateRange(date, date))
    for page in pages_to_process
    for date in date_range
]

data: list[dict[str, int]] = [{} for _ in date_range]
for future in concurrent.futures.as_completed(futures):
    try:
        page, date_range, view_count = future.result()
        data[days_to_index[date_range.start]][page] = view_count

    except Exception as e:
        print(f"Error processing page: {e}")

processor = BasicProcessor()

result = processor.process_test(data)
print(result)
