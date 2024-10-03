import concurrent.futures
from analytics_api.analytics_api import AnalyticsAPI
from dotenv import load_dotenv
from common.dates import Date, DateRange
from common.pages import PageMetadata
from processor.basic_processor import BasicProcessor
import matplotlib.pyplot as plt

load_dotenv(dotenv_path=".env")

api = AnalyticsAPI()
start_date = Date(day=1, month=7, year=2024)
date_range = DateRange(start=start_date, end=start_date.add_days(10))

pages_to_process = [
    "Earth",
    "Moon",
    # "Sun",
    # "Mars",
    # "Jupiter",
    # "Saturn",
    # "Uranus",
    # "Neptune",
    # "Pluto",
]

view_futures = [
    api.get_page_views(page, DateRange(date, date))
    for page in pages_to_process
    for date in date_range
]

edit_futures = [
    api.get_page_edits(page, DateRange(date, date))
    for page in pages_to_process
    for date in date_range
]

all_futures = {future: "view" for future in view_futures}
all_futures.update({future: "edit" for future in edit_futures})

data = {page: PageMetadata(page, date_range) for page in pages_to_process}
for future in concurrent.futures.as_completed(all_futures):
    future_type = all_futures[future]
    try:
        if future_type == "view":
            page, date_range, view_count = future.result()
            data[page].views.add_data_point(date_range.start, view_count)
        elif future_type == "edit":
            page, date_range, edit_count = future.result()
            data[page].net_bytes_difference.add_data_point(date_range.start, edit_count)

    except Exception as e:
        print(f"Error processing {future_type} future: {e}")

print(data)

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
