from functools import lru_cache
import concurrent.futures


from google.cloud import bigquery
from google.cloud.bigquery.table import Table
from google.cloud.bigquery.schema import SchemaField
from logger import Logger, Component

from .client_helpers import get_bigquery_client


class WikipediaDataAccessor:
    def __init__(
        self, logger: Logger, credentials_env_variable: str, buffer_size: int = 1000
    ):
        self.client = get_bigquery_client(credentials_env_variable)
        self.logger = logger
        self.dataset_id = "wikipedia_data"
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
        self.buffer_size = buffer_size

        self.write_buffer: list[dict] = []

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
        self.logger.info(
            f"Created table {table.project}.{table.dataset_id}.{table.table_id}",
            Component.DATABASE,
        )
        return table

    def delete_table(self, table_name: str) -> None:
        """
        Delete a table in BigQuery

        Args:
            table_name: ID for the table to delete
        """
        table_ref = f"{self.client.project}.{self.dataset_id}.{table_name}"
        self.client.delete_table(table_ref, not_found_ok=True)
        self.logger.info(f"Deleted table {table_name}", Component.DATABASE)

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

    def write_to_table(self, table: Table, rows: list[dict], run_async: bool) -> None:
        """
        Write data to a BigQuery table using load_table_from_json

        Args:
            table: Table instance to write to
            rows: List of dictionaries representing the rows to be inserted
            run_async: If True, the load job will be run in a separate thread
        """
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        )

        def load_job(buffer: list[dict]) -> None:
            try:
                load_job = self.client.load_table_from_json(
                    buffer, table, job_config=job_config
                )
                load_job.result()  # Wait for the job to complete
                self.logger.info(
                    f"Successfully loaded {len(buffer)} rows into {table}",
                    Component.DATABASE,
                )
            except Exception as e:
                self.logger.error(
                    f"Encountered error while loading rows: {e}", Component.DATABASE
                )

        self.write_buffer.extend(rows)

        if len(self.write_buffer) >= self.buffer_size:
            # Use ThreadPoolExecutor to run the load job in a separate thread
            if run_async:
                self.executor.submit(
                    load_job, self.write_buffer.copy()
                )  # NOTE: we should keep track of the future object to check for errors
            else:
                try:
                    load_job(self.write_buffer.copy())
                except Exception as e:
                    self.logger.error(f"Error in load job: {e}", Component.DATABASE)

            self.write_buffer = []
