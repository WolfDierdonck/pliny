from dotenv import load_dotenv

from common.dates import Date

from ingestion.processor.intermediate_table_processor import IntermediateTableProcessor
from ingestion.mediawiki_api.mediawiki_helper import MediaWikiHelper
from sql.wikipedia_data_accessor import WikipediaDataAccessor
from sql.intermediate_table_data import INTEMEDIATE_TABLE_SCHEMA

load_dotenv(dotenv_path=".env")

wikipedia_data_accessor = WikipediaDataAccessor("PLINY_BIGQUERY_SERVICE_ACCOUNT")
wikipedia_data_accessor.delete_table("intermediate_table")
wikipedia_data_accessor.create_table("intermediate_table", INTEMEDIATE_TABLE_SCHEMA)

start_page = "A"
for i in range(5):
    pages = []
    page_iterator = MediaWikiHelper.get_all_pages_iterator(start_page)
    for i in range(1000):
        next_page = next(page_iterator)
        pages.append(next_page)

    start_page = next(page_iterator)

    processor = IntermediateTableProcessor()
    processor.process(pages, Date(2024, 8, 6))

    print("In the future, we will start from the following page: " + start_page)
