from dotenv import load_dotenv
from common.dates import Date, DateRange
from common.time_series import TimeSeries
from ingestion.mediawiki_api.mediawiki_api import MediaWikiAPI
from ingestion.mediawiki_api.mediawiki_helper import MediaWikiHelper
from ingestion.processor.basic_processor import BasicProcessor
import random
from scoring.scorer.basic_scorer import BasicScorer
import experimentation.sample_articles

load_dotenv(dotenv_path=".env")

page_iterator = MediaWikiHelper.get_all_pages_iterator()
for i in range(100):
    next_page = next(page_iterator)
    print(next_page)
exit()

sample_articles = experimentation.sample_articles.early_august_articles

# Take 100 random articles to process
NUM_PAGES = 100
pages_to_process = random.sample(
    list(sample_articles), min(NUM_PAGES, len(sample_articles))
)

date_range = DateRange(Date(2024, 8, 5), Date(2024, 8, 8))

# Process each page for the entire date range. Each loop will process the overall score for all pages for a specific date.
processor = BasicProcessor()
scorer = BasicScorer()
scores_time_series = {page: TimeSeries(date_range) for page in pages_to_process}
for date in date_range:
    data = processor.process_pages(pages_to_process, date)
    scores = scorer.score(date, data).scores
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
