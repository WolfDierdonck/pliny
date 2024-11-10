from dotenv import load_dotenv
import time

from common.dates import Date, DateRange

from ingestion.processor.intermediate_table_processor import IntermediateTableProcessor
from ingestion.mediawiki_api.mediawiki_helper import MediaWikiHelper
from sql.wikipedia_data_accessor import WikipediaDataAccessor
from sql.intermediate_table_data import INTEMEDIATE_TABLE_SCHEMA
from ingestion.data_sources.page_revision_data_source import PageRevisionDumpFile
from ingestion.data_sources.page_view_data_source import PageViewDumpFile
from ingestion.wikimedia_dumps.dump_manager import DumpManager

load_dotenv(dotenv_path=".env")

START_PAGE = "1"
BATCH_SIZE = 1000
NUMBER_OF_BATCHES = 10000
BATCH_WAIT_TIME = 0.0

wikipedia_data_accessor = WikipediaDataAccessor("PLINY_BIGQUERY_SERVICE_ACCOUNT", buffer_size=10000)
wikipedia_data_accessor.delete_table("intermediate_table")
wikipedia_data_accessor.create_table("intermediate_table", INTEMEDIATE_TABLE_SCHEMA)

date_range = DateRange(Date(2024, 10, 1), Date(2024, 10, 1))

dump_manager = DumpManager("dumps", date_range)
revision_data_source = PageRevisionDumpFile(dump_manager)
view_data_source = PageViewDumpFile(dump_manager)

processor = IntermediateTableProcessor(revision_data_source, view_data_source, wikipedia_data_accessor)
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
