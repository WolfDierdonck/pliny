from google.cloud.bigquery.schema import SchemaField

INTEMEDIATE_TABLE_SCHEMA = [
    SchemaField("date", "DATE", mode="REQUIRED"),
    SchemaField("page_name", "STRING", mode="REQUIRED"),
    SchemaField("view_count", "INT64", mode="REQUIRED"),
    SchemaField("revision_count", "INT64", mode="REQUIRED"),
    SchemaField("net_bytes_change", "INT64", mode="REQUIRED"),
    SchemaField("editor_count", "INT64", mode="REQUIRED"),
    SchemaField("revert_count", "INT64", mode="REQUIRED"),
]


class IntermediateTableRow:
    def __init__(self, page_name: str):
        self.page_name = page_name
        self.view_count = float("nan")
        self.revision_count = float("nan")
        self.net_bytes_change = float("nan")
        self.editor_count = float("nan")
        self.revert_count = float("nan")

    def __str__(self) -> str:
        return f"{self.page_name}: view_count={self.view_count}, revision_count={self.revision_count}, net_bytes_change={self.net_bytes_change}, editor_count={self.editor_count}, revert_count={self.revert_count}"

    def __repr__(self) -> str:
        return f"IntermediateTableRow({self})"
