from datetime import timedelta
import time

from logger import Logger, Component
from common.dates import DateRange

from sql.wikipedia_data_accessor import WikipediaDataAccessor

from ingestion.processor.intermediate_table_processor import IntermediateTableProcessor
from ingestion.data_sources.page_revision_data_source import (
    PageRevisionAPI,
    PageRevisionDumpFile,
)
from ingestion.data_sources.page_view_data_source import PageViewAPI, PageViewDumpFile
from ingestion.data_sources.page_name_data_source import (
    PageNameDumpFile,
    PageNameWikiMediaAPI,
)
from ingestion.wikimedia_dumps.dump_manager import DumpManager
from sql.intermediate_table_data import recreate_intermediate_table


def ingest_dates(
    logger: Logger,
    date_range: DateRange,
    name_source_str: str,
    view_source_str: str,
    edit_source_str: str,
    batch_size: int,
    batch_wait: float,
    delete_dump_files: bool,
    recreate_table: bool = False,
) -> None:
    wikipedia_data_accessor = WikipediaDataAccessor(
        logger, "PLINY_BIGQUERY_SERVICE_ACCOUNT", buffer_size=batch_size * 10
    )

    if recreate_table:
        recreate_intermediate_table(wikipedia_data_accessor)

    dump_manager = DumpManager(logger, "dumps", date_range)

    view_source = (
        PageViewDumpFile(logger, dump_manager)
        if view_source_str == "dump"
        else PageViewAPI()
    )

    edit_source = (
        PageRevisionDumpFile(logger, dump_manager)
        if edit_source_str == "dump"
        else PageRevisionAPI()
    )

    processor = IntermediateTableProcessor(
        logger, edit_source, view_source, wikipedia_data_accessor
    )
    for date in date_range:
        pages = []
        try:
            logger.info(f"Starting ingestion for date {date}", Component.CORE)
            page_name_data_source = (
                PageNameDumpFile(date, dump_manager)
                if name_source_str == "dump"
                else PageNameWikiMediaAPI()
            )
            while True:

                for i in range(batch_size):
                    page = page_name_data_source.get_next_page_name()
                    if i == 0:
                        logger.info(
                            f"Just started an ingestion batch from page {page} for date {date}",
                            Component.CORE,
                        )

                    pages.append(page)

                processor.process(pages, date)
                pages = []

                if batch_wait > 0:
                    time.sleep(batch_wait)

        except StopIteration:
            if len(pages) > 0:
                processor.process(pages, date)

                t = wikipedia_data_accessor.get_table("intermediate_table")
                wikipedia_data_accessor.write_to_table(
                    t, [], run_async=False, flush_buffer=True
                )
                pages = []
            logger.info(f"Finished ingesting all pages for date {date}", Component.CORE)
            if delete_dump_files:
                dump_manager.delete_page_view_dump(date)
                logger.info(f"Deleted page view dump for date {date}", Component.CORE)

                next_day = date.to_py_date() + timedelta(days=1)
                if next_day.month != date.month:
                    dump_manager.delete_page_revision_dump(date)
                    logger.info(
                        f"Deleted page revision dump for date {date}", Component.CORE
                    )
            continue
