import requests
from common.pages import PageMetadata
from common.dates import Date, DateRange
from analytics_api.converters import AnalyticsAPIConverter


class AnalyticsAPI:
    def __init__(self) -> None:
        self.project = "en.wikipedia.org"
        self.url = "https://wikimedia.org/api/rest_v1/metrics"
        self.headers = {
            "User-Agent": "Pliny test",
            "From": "wolf.vandierdonck@gmail.com",
        }

    def get_page_views(self, page_name: str, date_range: DateRange) -> int:
        """
        Gets the number of views for a page between two dates
        https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html#get-number-of-page-views-for-a-page
        """
        access = "all-access"
        agent = "all-agents"
        granularity = "daily"

        date_range_str = AnalyticsAPIConverter.get_date_range_url_format(date_range)
        path = f"/pageviews/per-article/{self.project}/{access}/{agent}/{page_name}/{granularity}/{date_range_str}"
        url = self.url + path
        response = requests.get(url, headers=self.headers)
        data = response.json()

        if "items" not in data or len(data["items"]) == 0:
            raise ValueError(
                f"No items in response. Url: {url} Actual response: {data}"
            )

        if "views" not in data["items"][0] or not isinstance(
            data["items"][0]["views"], int
        ):
            raise ValueError("No integer views in response")

        return data["items"][0]["views"]

    def get_page_edits(self, page_name: str, date_range: DateRange) -> int:
        """
        Gets net byte difference for a page between two dates
        https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/edits.html#get-net-change-for-a-page-in-bytes
        """
        editor_type = "user"
        granularity = "daily"

        date_range_str = AnalyticsAPIConverter.get_date_range_url_format(date_range)
        path = f"/bytes-difference/net/per-page/{self.project}/{page_name}/{editor_type}/{granularity}/{date_range_str}"
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

        if "net_bytes_diff" not in result or not isinstance(
            result["net_bytes_diff"], int
        ):
            raise ValueError("No integer net_bytes_diff in response")

        return result["net_bytes_diff"]

    def get_most_edited_articles(self, date: Date) -> list[PageMetadata]:
        """
        Get top 100 pages by net bytes difference for a given date
        https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/edits.html#list-most-edited-pages-by-net-difference-in-bytes
        """
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
            rank = item["rank"]
            top_pages.append(PageMetadata(page_name, rank, byte_delta=byte_delta))

        return top_pages

    def get_most_viewed_articles(self, date: Date) -> list[PageMetadata]:
        """
        Get top 1000 pages by views for a given date
        https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html#list-most-viewed-pages
        """
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
            rank = item["rank"]
            top_pages.append(PageMetadata(page_name, rank, view_count=view_count))

        return top_pages
