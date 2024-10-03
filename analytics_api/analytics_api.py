import concurrent.futures
from concurrent.futures import Future
import requests
from common.dates import Date, DateRange
from analytics_api.converters import AnalyticsAPIConverter
from common.time_series import TimeSeries
import datetime


class AnalyticsAPI:
    def __init__(self) -> None:
        self.project = "en.wikipedia.org"
        self.url = "https://wikimedia.org/api/rest_v1/metrics"
        self.headers = {
            "User-Agent": "Pliny test",
            "From": "wolf.vandierdonck@gmail.com",
        }
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)

    def get_page_views(
        self, page_name: str, date_range: DateRange
    ) -> Future[tuple[str, DateRange, TimeSeries]]:
        """
        Gets the number of views for a page between two dates
        https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html#get-number-of-page-views-for-a-page
        """

        def fetch_and_process(
            page_name: str, date_range: DateRange
        ) -> tuple[str, DateRange, TimeSeries]:
            access = "all-access"
            agent = "all-agents"
            granularity = "daily"

            date_range_str = AnalyticsAPIConverter.get_date_range_url_format(date_range)
            path = f"/pageviews/per-article/{self.project}/{access}/{agent}/{page_name}/{granularity}/{date_range_str}"
            url = self.url + path

            response = requests.get(url, headers=self.headers)
            if (
                response.status_code == 404
            ):  # No data for this range (page just created)
                return page_name, date_range, TimeSeries(date_range)

            data = response.json()

            if "items" not in data or len(data["items"]) == 0:
                raise ValueError(
                    f"No items in response. Url: {url} Actual response: {data}"
                )

            time_series = TimeSeries(date_range)
            for item in data["items"]:
                timestamp: str = item["timestamp"]
                py_date = datetime.datetime.strptime(timestamp, "%Y%m%d%H").date()
                date = Date.from_py_date(py_date)
                views = item["views"]
                time_series.add_data_point(date, views)

            return page_name, date_range, time_series

        return self.executor.submit(fetch_and_process, page_name, date_range)

    def get_page_edits(
        self, page_name: str, date_range: DateRange
    ) -> Future[tuple[str, DateRange, TimeSeries]]:
        """
        Gets net byte difference for a page between two dates
        https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/edits.html#get-net-change-for-a-page-in-bytes
        """

        def fetch_and_process(
            page_name: str, date_range: DateRange
        ) -> tuple[str, DateRange, TimeSeries]:
            editor_type = "user"
            granularity = "daily"

            date_range_str = AnalyticsAPIConverter.get_date_range_url_format(date_range)
            path = f"/bytes-difference/net/per-page/{self.project}/{page_name}/{editor_type}/{granularity}/{date_range_str}"
            url = self.url + path
            response = requests.get(url, headers=self.headers)

            if (
                response.status_code == 404
            ):  # No data for this range (page just created or no edits)
                return page_name, date_range, TimeSeries(date_range)

            data = response.json()

            if "items" not in data or len(data["items"]) == 0:
                raise ValueError(
                    f"No items in response. Url: {url} Actual response: {data}"
                )

            item = data["items"][0]
            if "results" not in item or len(item["results"]) == 0:
                raise ValueError("No results in response")

            time_series = TimeSeries(date_range)
            for result in item["results"]:
                timestamp: str = result["timestamp"]
                py_date = datetime.datetime.strptime(
                    timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
                ).date()
                date = Date.from_py_date(py_date)

                net_bytes_diff = result["net_bytes_diff"]

                time_series.add_data_point(date, net_bytes_diff)

            return page_name, date_range, time_series

        return self.executor.submit(fetch_and_process, page_name, date_range)

    def get_most_edited_articles(
        self, date: Date
    ) -> Future[tuple[Date, list[tuple[str, float]]]]:
        """
        Get top 100 pages by net bytes difference for a given date. Output will be sorted by rank.
        https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/edits.html#list-most-edited-pages-by-net-difference-in-bytes
        """

        def fetch_and_process(date: Date) -> tuple[Date, list[tuple[str, float]]]:
            editor_type = "user"
            page_type = "content"

            date_str = AnalyticsAPIConverter.get_date_url_format(date)
            path = f"/edited-pages/top-by-net-bytes-difference/{self.project}/{editor_type}/{page_type}/{date_str}"
            url = self.url + path

            response = requests.get(url, headers=self.headers)
            data = response.json()

            if "items" not in data or len(data["items"]) == 0:
                raise ValueError(
                    f"No items in response. Url: {url} Actual response: {data}"
                )

            item = data["items"][0]
            if "results" not in item or len(item["results"]) == 0:
                raise ValueError("No results in response")

            result = item["results"][0]
            if "top" not in result or len(result["top"]) == 0:
                raise ValueError("No top in response")

            top = result["top"]
            top_pages = []
            for item in top:
                page_name = item["page_title"]
                byte_delta = item["net_bytes_diff"]
                top_pages.append((page_name, byte_delta))

            return date, top_pages

        return self.executor.submit(fetch_and_process, date)

    def get_most_viewed_articles(
        self, date: Date
    ) -> Future[tuple[Date, list[tuple[str, float]]]]:
        """
        Get top 1000 pages by views for a given date. Output will be sorted by rank.
        https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html#list-most-viewed-pages
        """

        def fetch_and_process(date: Date) -> tuple[Date, list[tuple[str, float]]]:
            access = "all-access"

            date_str = AnalyticsAPIConverter.get_date_url_format(date)
            path = f"/pageviews/top/{self.project}/{access}/{date_str}"
            url = self.url + path

            response = requests.get(url, headers=self.headers)
            data = response.json()

            if "items" not in data or len(data["items"]) == 0:
                raise ValueError(
                    f"No items in response. Url: {url} Actual response: {data}"
                )

            item = data["items"][0]

            if "articles" not in item or len(item["articles"]) == 0:
                raise ValueError("No articles in response")

            articles = item["articles"]
            top_pages = []
            for item in articles:
                page_name = item["article"]
                view_count = item["views"]
                top_pages.append((page_name, view_count))

            return date, top_pages

        return self.executor.submit(fetch_and_process, date)
