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
        SchemaField("abs_bytes_changed", "INT64", mode="REQUIRED"),
        SchemaField("avg_bytes_changed_per_edit", "FLOAT64", mode="REQUIRED"),
    ],
    "top_growing_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("net_bytes_changed", "INT64", mode="REQUIRED"),
    ],
    "top_shrinking_final_table": [
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
        SchemaField("avg_bytes_reverted_per_revert", "FLOAT64", mode="REQUIRED"),
    ],
    "top_views_gained_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("current_view_count", "INT64", mode="REQUIRED"),
        SchemaField("one_day_ago_view_count", "INT64", mode="NULLABLE"),
        SchemaField("two_days_ago_view_count", "INT64", mode="NULLABLE"),
        SchemaField("view_count_ratio", "FLOAT64", mode="REQUIRED"),
    ],
    "top_views_lost_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("current_view_count", "INT64", mode="REQUIRED"),
        SchemaField("one_day_ago_view_count", "INT64", mode="NULLABLE"),
        SchemaField("two_days_ago_view_count", "INT64", mode="NULLABLE"),
        SchemaField("view_count_ratio", "FLOAT64", mode="REQUIRED"),
    ],
    "top_views_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("page_name", "STRING", mode="REQUIRED"),
        SchemaField("view_count_0", "INT64", mode="REQUIRED"),
        SchemaField("view_count_1", "INT64", mode="NULLABLE"),
        SchemaField("view_count_2", "INT64", mode="NULLABLE"),
        SchemaField("view_count_3", "INT64", mode="NULLABLE"),
        SchemaField("view_count_4", "INT64", mode="NULLABLE"),
        SchemaField("view_count_5", "INT64", mode="NULLABLE"),
        SchemaField("view_count_6", "INT64", mode="NULLABLE"),
    ],
    "total_metadata_final_table": [
        SchemaField("date", "DATE", mode="REQUIRED"),
        SchemaField("total_edit_count", "INT64", mode="REQUIRED"),
        SchemaField("total_view_count", "INT64", mode="REQUIRED"),
        SchemaField("total_editor_count", "INT64", mode="REQUIRED"),
        SchemaField("total_revert_count", "INT64", mode="REQUIRED"),
        SchemaField("total_net_bytes_changed", "INT64", mode="REQUIRED"),
    ],
}

PARTITION_COLUMNS: dict[str, str] = {
    "top_editors_final_table": "date",
    "top_edits_final_table": "date",
    "top_growing_final_table": "date",
    "top_shrinking_final_table": "date",
    "top_vandalism_final_table": "date",
    "top_views_gained_final_table": "date",
    "top_views_lost_final_table": "date",
    "top_views_final_table": "date",
    "total_metadata_final_table": "date",
}


def score_dates(
    logger: Logger,
    date_range: DateRange,
    recreate_final_tables: bool,
    score_tables: list[str],
) -> None:
    wikipedia_data_accessor = WikipediaDataAccessor(
        logger, "PLINY_BIGQUERY_SERVICE_ACCOUNT", buffer_size=1
    )
    scorer = FinalTableScorer(logger, wikipedia_data_accessor, insert_limit=100)

    processed_score_tables = []
    if score_tables:
        for table in score_tables:
            table = f"{table}_final_table"
            if table not in FINAL_TABLE_SCHEMAS:
                logger.error(
                    f"Table {table} not found in final table schemas. Exiting",
                    Component.CORE,
                )
                exit()
            processed_score_tables.append(table)
    else:
        for table in FINAL_TABLE_SCHEMAS:
            processed_score_tables.append(table)

    if recreate_final_tables:
        logger.info("Recreating final tables", Component.CORE)
        for table_name in processed_score_tables:
            schema = FINAL_TABLE_SCHEMAS[table_name]
            wikipedia_data_accessor.delete_table(table_name)
            wikipedia_data_accessor.create_table(
                table_name,
                schema,
                partition_on_date=True,
                partition_column=PARTITION_COLUMNS[table_name],
            )

    for date in date_range:
        logger.info(f"Starting scoring for date {date}", Component.CORE)
        if "top_editors_final_table" in processed_score_tables:
            scorer.compute_top_editors(date)

        if "top_edits_final_table" in processed_score_tables:
            scorer.compute_top_edits(date)

        if "top_growing_final_table" in processed_score_tables:
            scorer.compute_top_growing(date)

        if "top_shrinking_final_table" in processed_score_tables:
            scorer.compute_top_shrinking(date)

        if "top_vandalism_final_table" in processed_score_tables:
            scorer.compute_top_vandalism(date)

        if "top_views_gained_final_table" in processed_score_tables:
            scorer.compute_top_views_gained(date)

        if "top_views_lost_final_table" in processed_score_tables:
            scorer.compute_top_views_lost(date)

        if "top_views_final_table" in processed_score_tables:
            scorer.compute_top_views(date)

        if "total_metadata_final_table" in processed_score_tables:
            scorer.compute_total_metadata(date)
