from datetime import timedelta
from logger import Logger, Component
from common.dates import Date
from sql.wikipedia_data_accessor import WikipediaDataAccessor
import os


class FinalTableScorer:
    def __init__(
        self,
        logger: Logger,
        wikipedia_data_accessor: WikipediaDataAccessor,
        insert_limit: int = 100,
    ) -> None:
        self.wikipedia_data_accessor = wikipedia_data_accessor
        self.insert_limit = insert_limit
        self.logger = logger

        current_file_path = os.path.abspath(
            __file__
        )  # Get the absolute path of the current file
        base_path = os.path.dirname(
            os.path.dirname(current_file_path)
        )  # Get the parent parent directory
        sql_path = os.path.join(base_path, "queries")

        # Read all files in the queries directory
        all_query_files = os.listdir(sql_path)
        self.queries = {}
        for query_file in all_query_files:
            with open(os.path.join(sql_path, query_file)) as f:
                self.queries[query_file] = f.read()

    def _run_query(self, file_name: str, params: dict[str, str]) -> None:
        query_template = self.queries[file_name]
        for key, value in params.items():
            query_template = query_template.replace("{{" + key + "}}", value)

        self.wikipedia_data_accessor.client.query_and_wait(query_template)

    def _get_sql_date(self, date: Date) -> str:
        return f"'{date.year}-{date.month:02d}-{date.day:02d}'"

    def _get_date_selection_str(self, date: Date, lookback_days: int) -> str:
        s = f"date={self._get_sql_date(date)}"
        for i in range(1, lookback_days):
            lookback_date = Date.from_py_date(date.to_py_date() - timedelta(days=i))
            s += f" OR date={self._get_sql_date(lookback_date)}"

        return s

    def compute_top_editors(self, date: Date) -> None:
        self.logger.info(f"Computing top editors for {date}", Component.DATABASE)

        file_name = "insert_top_editors.sql"
        params = {
            "date": self._get_sql_date(date),
            "dateSelectionStr": self._get_date_selection_str(date, 3),
            "limit": str(self.insert_limit),
        }

        self._run_query(file_name, params)

    def compute_top_edits(self, date: Date) -> None:
        self.logger.info(f"Computing top edits for {date}", Component.DATABASE)

        file_name = "insert_top_edits.sql"
        params = {
            "date": self._get_sql_date(date),
            "dateSelectionStr": self._get_date_selection_str(date, 3),
            "limit": str(self.insert_limit),
        }

        self._run_query(file_name, params)

    def compute_top_growing(self, date: Date) -> None:
        self.logger.info(f"Computing top growing for {date}", Component.DATABASE)

        file_name = "insert_top_growing.sql"
        params = {
            "date": self._get_sql_date(date),
            "dateSelectionStr": self._get_date_selection_str(date, 3),
            "limit": str(self.insert_limit),
        }

        self._run_query(file_name, params)
    
    def compute_top_shrinking(self, date: Date) -> None:
        self.logger.info(f"Computing top shrinking for {date}", Component.DATABASE)

        file_name = "insert_top_shrinking.sql"
        params = {
            "date": self._get_sql_date(date),
            "dateSelectionStr": self._get_date_selection_str(date, 3),
            "limit": str(self.insert_limit),
        }

        self._run_query(file_name, params)

    def compute_top_vandalism(self, date: Date) -> None:
        self.logger.info(f"Computing top vandalism for {date}", Component.DATABASE)

        file_name = "insert_top_vandalism.sql"
        params = {
            "date": self._get_sql_date(date),
            "dateSelectionStr": self._get_date_selection_str(date, 3),
            "limit": str(self.insert_limit),
        }

        self._run_query(file_name, params)

    def compute_top_views_gained(self, date: Date) -> None:
        self.logger.info(f"Computing top views gained for {date}", Component.DATABASE)

        previous_date = Date.from_py_date(date.to_py_date() - timedelta(days=1))

        file_name = "insert_top_views_gained.sql"
        params = {
            "todayDate": self._get_sql_date(date),
            "yesterdayDate": self._get_sql_date(previous_date),
            "limit": str(self.insert_limit),
        }

        self._run_query(file_name, params)
    
    def compute_top_views_lost(self, date: Date) -> None:
        self.logger.info(f"Computing top views lost for {date}", Component.DATABASE)

        previous_date = Date.from_py_date(date.to_py_date() - timedelta(days=1))

        file_name = "insert_top_views_lost.sql"
        params = {
            "todayDate": self._get_sql_date(date),
            "yesterdayDate": self._get_sql_date(previous_date),
            "limit": str(self.insert_limit),
        }

        self._run_query(file_name, params)

    def compute_top_views(self, date: Date) -> None:
        self.logger.info(f"Computing top views for {date}", Component.DATABASE)

        file_name = "insert_top_views.sql"
        params = {
            "date": self._get_sql_date(date),
            "dateSelectionStr": self._get_date_selection_str(date, 3),
            "limit": str(self.insert_limit),
        }

        self._run_query(file_name, params)

    def compute_total_metadata(self, date: Date) -> None:
        self.logger.info(f"Computing total metadata for {date}", Component.DATABASE)

        file_name = "insert_total_metadata.sql"
        params = {
            "date": self._get_sql_date(date),
        }

        self._run_query(file_name, params)
