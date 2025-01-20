from google.cloud.bigquery.schema import SchemaField
from sql.wikipedia_data_accessor import WikipediaDataAccessor

INTERMEDIATE_TABLE_SCHEMA = [
    SchemaField("date", "DATE", mode="REQUIRED"),
    SchemaField("page_name", "STRING", mode="REQUIRED"),
    SchemaField("view_count", "INT64", mode="REQUIRED"),
    SchemaField("edit_count", "INT64", mode="REQUIRED"),
    SchemaField("revert_count", "INT64", mode="REQUIRED"),
    SchemaField("editor_count", "INT64", mode="REQUIRED"),
    SchemaField("total_bytes_changed", "INT64", mode="REQUIRED"),
    SchemaField("total_bytes_reverted", "INT64", mode="REQUIRED"),
]


def recreate_intermediate_table(wikipedia_data_accessor: WikipediaDataAccessor) -> None:
    wikipedia_data_accessor.delete_table("intermediate_table")
    wikipedia_data_accessor.create_table(
        "intermediate_table", INTERMEDIATE_TABLE_SCHEMA
    )


class IntermediateTableRow:
    def __init__(self, page_name: str):
        self.page_name = page_name
        self.view_count = 0
        self.edit_count = 0
        self.total_bytes_changed = 0
        self.editor_count = 0
        self.revert_count = 0
        self.total_bytes_reverted = 0

    def __str__(self) -> str:
        return f"{self.page_name}: view_count={self.view_count}, edit_count={self.edit_count}, total_bytes_changed={self.total_bytes_changed}, editor_count={self.editor_count}, revert_count={self.revert_count} total_bytes_reverted={self.total_bytes_reverted}"

    def __repr__(self) -> str:
        return f"IntermediateTableRow({self})"
