from dotenv import load_dotenv
import time

from common.dates import Date, DateRange

from ingestion.processor.intermediate_table_processor import IntermediateTableProcessor
from ingestion.mediawiki_api.mediawiki_helper import MediaWikiHelper
from sql.wikipedia_data_accessor import WikipediaDataAccessor
from sql.intermediate_table_data import INTEMEDIATE_TABLE_SCHEMA

load_dotenv(dotenv_path=".env")

wikipedia_data_accessor = WikipediaDataAccessor("PLINY_BIGQUERY_SERVICE_ACCOUNT")
wikipedia_data_accessor.delete_table("intermediate_table")
wikipedia_data_accessor.create_table("intermediate_table", INTEMEDIATE_TABLE_SCHEMA)

date_range = DateRange(Date(2024, 8, 5), Date(2024, 8, 7))

START_PAGE = "A"
BATCH_SIZE = 100
NUMBER_OF_BATCHES = 10000
BATCH_WAIT_TIME = 0.7

processor = IntermediateTableProcessor()
for date in date_range:
    page_iterator = MediaWikiHelper.get_all_pages_iterator(START_PAGE)
    for i in range(NUMBER_OF_BATCHES):
        pages = []

        for i in range(BATCH_SIZE):
            page = next(page_iterator)
            if i == 0:
                print("Just started a batch from page", page, "for date", date)

            pages.append(page)

        processor.process(pages, date)
        time.sleep(BATCH_WAIT_TIME)
