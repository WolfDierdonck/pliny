from datetime import date, timedelta


class Date:
    def __init__(self, year: int, month: int, day: int) -> None:
        self.year = year
        self.month = month
        self.day = day

    def __str__(self) -> str:
        return f"year: {self.year} month: {self.month} day: {self.day}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            return False

        return (
            self.year == other.year
            and self.month == other.month
            and self.day == other.day
        )


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

            result = Date(
                year=self.current.year,
                month=self.current.month,
                day=self.current.day,
            )

            py_date = date(self.current.year, self.current.month, self.current.day)
            next_py_date = py_date + timedelta(days=1)
            self.current = Date(
                year=next_py_date.year,
                month=next_py_date.month,
                day=next_py_date.day,
            )

            return result

    def __iter__(self) -> DateRangeIterator:
        return DateRange.DateRangeIterator(self.start, self.end)
