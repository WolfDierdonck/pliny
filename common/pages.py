from .time_series import TimeSeries
from .dates import DateRange


class PageMetadata:
    def __init__(self, name: str, date_range: DateRange) -> None:
        self.name = name
        self.views = TimeSeries(date_range)
        self.net_bytes_difference = TimeSeries(date_range)

    def __str__(self) -> str:
        return f"{self.name}:\n\tViews: {self.views}\n\tNet Bytes Difference: {self.net_bytes_difference}\n"

    def __repr__(self) -> str:
        return f"PageMetadata({self})"
