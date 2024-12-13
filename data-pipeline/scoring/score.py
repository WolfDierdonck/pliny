from logger import Component, Logger

from common.dates import DateRange

from sql.wikipedia_data_accessor import WikipediaDataAccessor

from scoring.scorer.final_table_scorer import FinalTableScorer


def score_dates(logger: Logger, date_range: DateRange) -> None:
    wikipedia_data_accessor = WikipediaDataAccessor(
        logger, "PLINY_BIGQUERY_SERVICE_ACCOUNT", buffer_size=1
    )
    scorer = FinalTableScorer(logger, wikipedia_data_accessor, insert_limit=100)

    for date in date_range:
        logger.info(f"Starting scoring for date {date}", Component.CORE)
        scorer.compute_top_views(date)
        scorer.compute_top_vandalism(date)
