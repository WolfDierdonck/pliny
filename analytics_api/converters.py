from common.dates import Date, DateRange


class AnalyticsAPIConverter:
    @staticmethod
    def get_date_url_format(date: Date) -> str:
        padded_year = str(date.year)
        padded_month = str(date.month).zfill(2)
        padded_day = str(date.day).zfill(2)
        return f"{padded_year}/{padded_month}/{padded_day}"

    @staticmethod
    def get_date_range_url_format(date_range: DateRange) -> str:
        def convert_date(date: Date) -> str:
            padded_year = str(date.year)
            padded_month = str(date.month).zfill(2)
            padded_day = str(date.day).zfill(2)
            return f"{padded_year}{padded_month}{padded_day}"

        start_date = date_range.start
        end_date = date_range.end
        return f"{convert_date(start_date)}/{convert_date(end_date)}"
