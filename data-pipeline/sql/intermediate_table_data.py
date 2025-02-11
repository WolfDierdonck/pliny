from google.cloud.bigquery.schema import SchemaField
from sql.wikipedia_data_accessor import WikipediaDataAccessor

INTERMEDIATE_TABLE_SCHEMA = [
    SchemaField("date", "DATE", mode="REQUIRED"),
    SchemaField("page_name", "STRING", mode="REQUIRED"),
    SchemaField("view_count", "INT64", mode="REQUIRED"),
    SchemaField("edit_count", "INT64", mode="REQUIRED"),
    SchemaField("revert_count", "INT64", mode="REQUIRED"),
    SchemaField("editor_count", "INT64", mode="REQUIRED"),
    SchemaField("net_bytes_changed", "INT64", mode="REQUIRED"),
    SchemaField("abs_bytes_changed", "INT64", mode="REQUIRED"),
    SchemaField("abs_bytes_reverted", "INT64", mode="REQUIRED"),
]


def recreate_intermediate_table(wikipedia_data_accessor: WikipediaDataAccessor) -> None:
    wikipedia_data_accessor.delete_table("intermediate_table")
    wikipedia_data_accessor.create_table(
        "intermediate_table", INTERMEDIATE_TABLE_SCHEMA, partition_on_date=True
    )


class IntermediateTableRow:
    def __init__(self, page_name: str):
        self.page_name = page_name
        self.view_count = 0
        self.edit_count = 0
        self.editor_count = 0
        self.revert_count = 0
        self.net_bytes_changed = 0
        self.abs_bytes_changed = 0
        self.abs_bytes_reverted = 0

    def __str__(self) -> str:
        return f"{self.page_name}: view_count={self.view_count}, edit_count={self.edit_count}, editor_count={self.editor_count}, revert_count={self.revert_count}, net_bytes_changed={self.net_bytes_changed}, abs_bytes_changed={self.abs_bytes_changed}, abs_bytes_reverted={self.abs_bytes_reverted}"

    def __repr__(self) -> str:
        return f"IntermediateTableRow({self})"
