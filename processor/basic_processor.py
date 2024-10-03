from common.dates import DateRange
from common.score import BasicScore
from common.time_series import TimeSeries
from common.pages import PageMetadata


class BasicProcessor:
    def __init__(self) -> None:
        pass

    def process_test(self, data: dict[str, PageMetadata]) -> BasicScore:
        """
        Return the score for each page/day. Here, the score is simple its view delta from the previous day.
        """
        scores = {
            key: TimeSeries(
                DateRange(
                    data[key].views.date_range.start.add_days(1),
                    data[key].views.date_range.end,
                )
            )
            for key in data
        }
        for key, page_metadata in data.items():
            for day in page_metadata.views.date_range:
                if day == page_metadata.views.date_range.start:
                    continue
                previous_day = day.add_days(-1)
                delta = page_metadata.views.get_data_point(
                    day
                ) - page_metadata.views.get_data_point(previous_day)
                scores[key].add_data_point(day, delta)

        return BasicScore(scores)
