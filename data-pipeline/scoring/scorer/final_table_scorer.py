from logger import Logger, Component
from common.dates import Date
from sql.wikipedia_data_accessor import WikipediaDataAccessor


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

    def _get_sql_date(self, date: Date) -> str:
        return f"'{date.year}-{date.month:02d}-{date.day:02d}'"

    def compute_top_views(self, date: Date) -> None:
        wda = self.wikipedia_data_accessor

        query = f"""
            INSERT INTO wikipedia_data.top_views_final_table (
                select date, page_name as 'article', view_count as 'views'
                from (
                    SELECT date, page_name, view_count
                    FROM wikipedia_data.intermediate_table_sep
                    where date={self._get_sql_date(date)}
                )
                order by views desc
                limit {self.insert_limit}
            )
        """

        self.logger.info(f"Computing top views for {date}", Component.DATABASE)
        wda.client.query_and_wait(query)

    def compute_top_vandalism(self, date: Date) -> None:
        wda = self.wikipedia_data_accessor

        query = f"""
            INSERT INTO wikipedia_data.top_vandalism_final_table (
                select date, page_name as 'article', log(revert_count) + log(net_bytes_change) as 'score' from (
                    SELECT page_name, revert_count, net_bytes_change, date
                    FROM wikipedia_data. intermediate_table_sep
                    where date={self._get_sql_date(date)} and revert_count > 0 and net_bytes_change > 0
                )
                order by score desc
                limit {self.insert_limit}
            )
        """

        self.logger.info(f"Computing top vandalism for {date}", Component.DATABASE)
        wda.client.query_and_wait(query)
