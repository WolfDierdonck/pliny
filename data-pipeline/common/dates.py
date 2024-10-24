from datetime import date, timedelta
from functools import total_ordering


@total_ordering
class Date:
    def __init__(self, year: int, month: int, day: int) -> None:
        self.year = year
        self.month = month
        self.day = day

    def __str__(self) -> str:
        padded_year = str(self.year)
        padded_month = str(self.month).zfill(2)
        padded_day = str(self.day).zfill(2)
        return f"{padded_year}/{padded_month}/{padded_day}"

    def __repr__(self) -> str:
        return f"Date({self})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            print("Warning: comparing Date with non-Date")
            return False

        return (
            self.year == other.year
            and self.month == other.month
            and self.day == other.day
        )

    def __hash__(self) -> int:
        return hash((self.year, self.month, self.day))

    def to_py_date(self) -> date:
        return date(self.year, self.month, self.day)

    @staticmethod
    def from_py_date(py_date: date) -> "Date":
        return Date(year=py_date.year, month=py_date.month, day=py_date.day)

    def add_days(self, days: int) -> "Date":
        new_py_date = self.to_py_date() + timedelta(days=days)
        return Date.from_py_date(new_py_date)

    def __lt__(self, other: "Date") -> bool:
        return self.to_py_date() < other.to_py_date()


class DateRange:
    def __init__(self, start: Date, end: Date):
        self.start = start
        self.end = end

    class DateRangeIterator:
        def __init__(self, start: Date, end: Date):
            self.current = start
            self.end = end
            self.stop = False

        def __next__(self) -> Date:
            if self.stop:
                raise StopIteration

            if self.current == self.end:
                self.stop = True

            result = self.current

            self.current = self.current.add_days(1)

            return result

    def __iter__(self) -> DateRangeIterator:
        return DateRange.DateRangeIterator(self.start, self.end)

    def __len__(self) -> int:
        start_date = self.start.to_py_date()
        end_date = self.end.to_py_date()
        return (end_date - start_date).days + 1

    def __str__(self) -> str:
        return f"{self.start} to {self.end}"

    def __repr__(self) -> str:
        return f"DateRange({self})"
