import concurrent.futures
from analytics_api.analytics_api import AnalyticsAPI
from dotenv import load_dotenv
from common.dates import Date, DateRange
from common.time_series import TimeSeries
from processor.basic_processor import BasicProcessor
import random

load_dotenv(dotenv_path=".env")

api = AnalyticsAPI()
start_date = Date(day=5, month=8, year=2024)
date_range = DateRange(start=start_date, end=start_date.add_days(3))

# 1. Get the most edited articles for each day in the date range
most_edited_articles: set[str] = set()
most_edited_futures = [api.get_most_edited_articles(date) for date in date_range]

for future in concurrent.futures.as_completed(most_edited_futures):
    try:
        date, articles = future.result()
        most_edited_articles.update(map(lambda x: x[0], articles))
    except Exception as e:
        print(f"Error processing most edited future: {e}")

# Take 100 random articles to process
NUM_PAGES = 50
pages_to_process = random.sample(
    list(most_edited_articles), min(NUM_PAGES, len(most_edited_articles))
)

# Process each page for the entire date range. Each loop will process the overall score for all pages for a specific date.
processor = BasicProcessor()
scores_time_series = {page: TimeSeries(date_range) for page in pages_to_process}
for date in date_range:
    scores = processor.process_pages(pages_to_process, date).scores
    for page, score in scores.items():
        scores_time_series[page].add_data_point(date, score)

for date in date_range:
    top_scores = []

    for page, time_series in scores_time_series.items():
        score = time_series.get_data_point(date)
        top_scores.append((score, page))

    # Sort the list in descending order based on the scores
    top_scores.sort(reverse=True, key=lambda x: x[0])

    # Print the top 5 entries
    print("Date:", date)
    for score, page in top_scores[:5]:
        print("Page:", page, "Score:", score)

    print("------")
