from common.dates import Date, DateRange


class TimeSeries:
    def __init__(self, date_range: DateRange) -> None:
        self.date_range = date_range
        self.values: list[float] = [float("nan")] * len(date_range)

        self.days_to_index: dict[Date, int] = {}
        i = 0
        for date in date_range:
            self.days_to_index[date] = i
            i += 1

    def add_data_point(self, date: Date, views: float) -> None:
        if date not in self.days_to_index:
            raise ValueError(f"Date {date} not in date range {self.date_range}")
        index = self.days_to_index[date]
        self.values[index] = views

    def get_data_point(self, date: Date) -> float:
        if date not in self.days_to_index:
            raise ValueError(f"Date {date} not in date range {self.date_range}")
        index = self.days_to_index[date]
        return self.values[index]

    def __len__(self) -> int:
        return len(self.values)

    def __str__(self) -> str:
        return f"{self.date_range}: {self.values}"

    def __repr__(self) -> str:
        return f"TimeSeries({self})"
