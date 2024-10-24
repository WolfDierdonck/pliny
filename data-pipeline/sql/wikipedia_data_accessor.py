from functools import lru_cache

from google.cloud import bigquery
from google.cloud.bigquery.table import Table
from google.cloud.bigquery.schema import SchemaField

from .client_helpers import get_bigquery_client


class WikipediaDataAccessor:
    def __init__(self, credentials_env_variable: str):
        self.client = get_bigquery_client(credentials_env_variable)
        self.dataset_id = "wikipedia_data"

    def create_table(self, table_name: str, schema: list[SchemaField]) -> Table:
        """
        Create a new table in BigQuery

        Args:
            table_name: ID for the new table
            schema: List of SchemaField objects defining the table structure

        Returns:
            Created Table instance
        """
        table_ref = f"{self.client.project}.{self.dataset_id}.{table_name}"
        table = Table(table_ref, schema=schema)
        table = self.client.create_table(table, exists_ok=True)
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
        return table

    def delete_table(self, table_name: str) -> None:
        """
        Delete a table in BigQuery

        Args:
            table_name: ID for the table to delete
        """
        table_ref = f"{self.client.project}.{self.dataset_id}.{table_name}"
        self.client.delete_table(table_ref, not_found_ok=True)
        print(f"Deleted table {table_name}")

    @lru_cache(maxsize=128)
    def get_table(self, table_name: str) -> Table:
        """
        Get a reference to an existing table in BigQuery

        Args:
            table_name: ID for the table

        Returns:
            Table instance
        """
        table_ref = f"{self.client.project}.{self.dataset_id}.{table_name}"
        return self.client.get_table(table_ref)

    def read_from_table(self, table: Table) -> list[dict]:
        """
        Read data from a BigQuery table using the table's read_rows method

        Args:
            table: Table instance to read from

        Returns:
            List of dictionaries representing the rows read
        """
        rows = self.client.list_rows(table)
        return [dict(row.items()) for row in rows]

    def write_to_table(self, table: Table, rows: list[dict]) -> None:
        """
        Write data to a BigQuery table using load_table_from_json

        Args:
            table: Table instance to write to
            rows: List of dictionaries representing the rows to be inserted
        """
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        )

        try:
            load_job = self.client.load_table_from_json(
                rows, table, job_config=job_config
            )
            load_job.result()  # Wait for the job to complete
            print(f"Successfully loaded {len(rows)} rows into {table}")
        except Exception as e:
            print(f"Encountered error while loading rows: {e}")
