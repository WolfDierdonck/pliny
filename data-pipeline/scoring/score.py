from logger import Component, Logger

from common.dates import DateRange

from sql.wikipedia_data_accessor import WikipediaDataAccessor
from google.cloud.bigquery.schema import SchemaField

from scoring.scorer.final_table_scorer import FinalTableScorer

FINAL_TABLE_SCHEMAS: dict[str, list[SchemaField]] = {
    "top_editors_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("editor_count", "INT64", mode="REQUIRED"),
    ],
    "top_edits_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("edit_count", "INT64", mode="REQUIRED"),
    ],
    "top_growing_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("net_bytes_changed", "INT64", mode="REQUIRED"),
    ],
    "top_vandalism_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("view_count", "INT64", mode="REQUIRED"),
        SchemaField("revert_count", "INT64", mode="REQUIRED"),
        SchemaField("abs_bytes_reverted", "INT64", mode="REQUIRED"),
        SchemaField("edit_count", "INT64", mode="REQUIRED"),
        SchemaField("percent_reverted", "FLOAT64", mode="REQUIRED"),
    ],
    "top_view_delta_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("current_view_count", "INT64", mode="REQUIRED"),
        SchemaField("previous_view_count", "INT64", mode="REQUIRED"),
        SchemaField("view_count_ratio", "INT64", mode="REQUIRED"),
    ],
    "top_views_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("view_count", "INT64", mode="REQUIRED"),
    ],
    "total_metadata_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("total_edit_count", "INT64", mode="REQUIRED"),
        SchemaField("total_view_count", "INT64", mode="REQUIRED"),
        SchemaField("total_editor_count", "INT64", mode="REQUIRED"),
        SchemaField("total_revert_count", "INT64", mode="REQUIRED"),
    ],
    "wikipedia_growth_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("wikipedia_growth_bytes", "INT64", mode="REQUIRED"),
    ],
}

PARTITION_COLUMNS: dict[str, str] = {
    "top_editors_final_table": "date",
    "top_edits_final_table": "date",
    "top_growing_final_table": "date",
    "top_vandalism_final_table": "date",
    "top_view_delta_final_table": "date",
    "top_views_final_table": "date",
    "total_metadata_final_table": "date",
    "wikipedia_growth_final_table": "date",
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
                table_name,
                schema,
                partition_on_date=True,
                partition_column=PARTITION_COLUMNS[table_name],
            )

    for date in date_range:
        logger.info(f"Starting scoring for date {date}", Component.CORE)
        scorer.compute_top_editors(date)
        scorer.compute_top_edits(date)
        scorer.compute_top_growing(date)
        scorer.compute_top_vandalism(date)
        scorer.compute_top_view_delta(date)
        scorer.compute_top_views(date)
        scorer.compute_total_metadata(date)
        scorer.compute_wikipedia_growth(date)
