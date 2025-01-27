from logger import Component, Logger

from common.dates import DateRange

from sql.wikipedia_data_accessor import WikipediaDataAccessor
from google.cloud.bigquery.schema import SchemaField

from scoring.scorer.final_table_scorer import FinalTableScorer

FINAL_TABLE_SCHEMAS: dict[str, list[SchemaField]] = {
    "top_views_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("view_count", "INT64", mode="REQUIRED"),
    ],
    "mock_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
    ],
}


def score_dates(
    logger: Logger, date_range: DateRange, recreate_final_tables: bool
) -> None:
    wikipedia_data_accessor = WikipediaDataAccessor(
        logger, "PLINY_BIGQUERY_SERVICE_ACCOUNT", buffer_size=1
    )
    scorer = FinalTableScorer(logger, wikipedia_data_accessor, insert_limit=100)

    if recreate_final_tables:
        logger.info("Recreating final tables", Component.CORE)
        for table_name, schema in FINAL_TABLE_SCHEMAS.items():
            wikipedia_data_accessor.delete_table(table_name)
            wikipedia_data_accessor.create_table(
                table_name, schema, partition_on_date=True
            )

    for date in date_range:
        logger.info(f"Starting scoring for date {date}", Component.CORE)
        scorer.compute_top_views(date)
        scorer.compute_mock(date)
