import concurrent.futures
from analytics_api.analytics_api import AnalyticsAPI
from dotenv import load_dotenv
from common.dates import Date, DateRange
from common.time_series import TimeSeries
from processor.basic_processor import BasicProcessor
import matplotlib.pyplot as plt

load_dotenv(dotenv_path=".env")

api = AnalyticsAPI()
start_date = Date(day=1, month=7, year=2024)
date_range = DateRange(start=start_date, end=start_date.add_days(10))

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

futures = [
    api.get_page_views(page, DateRange(date, date))
    for page in pages_to_process
    for date in date_range
]

data = {page: TimeSeries(date_range) for page in pages_to_process}
for future in concurrent.futures.as_completed(futures):
    try:
        page, date_range, view_count = future.result()
        data[page].add_data_point(date_range.start, view_count)

    except Exception as e:
        print(f"Error processing page: {e}")

processor = BasicProcessor()

scores = processor.process_test(data).scores

# Plot each key in the dictionary as a separate line
for key, time_series in scores.items():
    plt.plot(time_series.values, label=key)

# Add labels and title
plt.xlabel("Time Unit")
plt.ylabel("Score")
plt.title("Scores Line Chart")
plt.legend()

# Show the plot
plt.show()
