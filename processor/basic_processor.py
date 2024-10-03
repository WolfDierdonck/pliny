from common.dates import DateRange
from common.score import BasicScore
from common.time_series import TimeSeries


class BasicProcessor:
    def __init__(self) -> None:
        pass

    def process_test(self, data: dict[str, TimeSeries]) -> BasicScore:
        """
        Return the score for each page/day. Here, the score is simple its view delta from the previous day.
        """
        scores = {
            key: TimeSeries(
                DateRange(
                    data[key].date_range.start.add_days(1), data[key].date_range.end
                )
            )
            for key in data
        }
        for key, time_series in data.items():
            for day in time_series.date_range:
                if day == time_series.date_range.start:
                    continue
                previous_day = day.add_days(-1)
                delta = time_series.get_data_point(day) - time_series.get_data_point(
                    previous_day
                )
                scores[key].add_data_point(day, delta)

        return BasicScore(scores)
