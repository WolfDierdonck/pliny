from dotenv import load_dotenv
import time

from common.dates import Date, DateRange

from ingestion.processor.intermediate_table_processor import IntermediateTableProcessor
from sql.wikipedia_data_accessor import WikipediaDataAccessor
from sql.intermediate_table_data import INTEMEDIATE_TABLE_SCHEMA
from ingestion.data_sources.page_revision_data_source import PageRevisionDumpFile
from ingestion.data_sources.page_view_data_source import PageViewDumpFile
from ingestion.data_sources.page_name_data_source import PageNameDumpFile
from ingestion.wikimedia_dumps.dump_manager import DumpManager
from logger import Logger, Component

load_dotenv(dotenv_path=".env")

BATCH_SIZE = 10000
BATCH_WAIT_TIME = 0.0

logger = Logger("data-pipeline")

wikipedia_data_accessor = WikipediaDataAccessor(
    logger, "PLINY_BIGQUERY_SERVICE_ACCOUNT", buffer_size=100000
)
# wikipedia_data_accessor.delete_table("intermediate_table")
# wikipedia_data_accessor.create_table("intermediate_table", INTEMEDIATE_TABLE_SCHEMA)

date_range = DateRange(Date(2024, 9, 4), Date(2024, 9, 6))

dump_manager = DumpManager(logger, "dumps", date_range)
revision_data_source = PageRevisionDumpFile(logger, dump_manager)
view_data_source = PageViewDumpFile(logger, dump_manager)

processor = IntermediateTableProcessor(
    logger, revision_data_source, view_data_source, wikipedia_data_accessor
)
for date in date_range:
    pages = []
    try:
        page_name_data_source = PageNameDumpFile(date, dump_manager)
        while True:

            for i in range(BATCH_SIZE):
                page = page_name_data_source.get_next_page_name()
                if i == 0:
                    logger.info(
                        f"Just started a batch from page {page} for date {date}",
                        Component.CORE,
                    )

                pages.append(page)

            processor.process(pages, date)
            pages = []

            if BATCH_WAIT_TIME > 0:
                time.sleep(BATCH_WAIT_TIME)

    except StopIteration:
        if len(pages) > 0:
            processor.process(pages, date)

            t = wikipedia_data_accessor.get_table("intermediate_table")
            wikipedia_data_accessor.write_to_table(
                t, [], run_async=False, buffer_load=False
            )
            pages = []
        logger.info(f"Finished processing all pages for date {date}", Component.CORE)
        continue
