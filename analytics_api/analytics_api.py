import requests
from common.pages import PageMetadata
from common.dates import Date


class AnalyticsAPI:
    def __init__(self) -> None:
        self.project = "en.wikipedia.org"
        self.url = "https://wikimedia.org/api/rest_v1/metrics"
        self.headers = {
            "User-Agent": "Pliny test",
            "From": "wolf.vandierdonck@gmail.com",
        }

    def get_page_views(self, page_name: str, start_date: Date, end_date: Date) -> int:
        access = "all-access"
        agent = "all-agents"
        granularity = "daily"
        path = f"/pageviews/per-article/{self.project}/{access}/{agent}/{page_name}/{granularity}/{start_date}/{end_date}"
        url = self.url + path
        response = requests.get(url, headers=self.headers)
        data = response.json()

        if "items" not in data or len(data["items"]) == 0:
            raise ValueError("No items in response")

        if "views" not in data["items"][0] or not isinstance(
            data["items"][0]["views"], int
        ):
            raise ValueError("No integer views in response")

        return data["items"][0]["views"]

    def get_page_edits(self, page_name: str, start_date: Date, end_date: Date) -> int:
        editor_type = "user"
        granularity = "daily"
        path = f"/bytes-difference/net/per-page/{self.project}/{page_name}/{editor_type}/{granularity}/{start_date}/{end_date}"
        url = self.url + path
        response = requests.get(url, headers=self.headers)
        data = response.json()

        if "items" not in data or len(data["items"]) == 0:
            raise ValueError("No items in response")

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
        editor_type = "user"
        page_type = "content"
        path = f"/edited-pages/top-by-net-bytes-difference/{self.project}/{editor_type}/{page_type}/{date}"
        url = self.url + path

        response = requests.get(url, headers=self.headers)
        data = response.json()
        top_pages = []
        for item in data["items"][0]["results"][0]["top"]:
            page_name = item["page_title"]
            byte_delta = item["net_bytes_diff"]
            rank = item["rank"]
            top_pages.append(PageMetadata(page_name, rank, byte_delta=byte_delta))

        return top_pages

    def get_most_viewed_articles(self, date: Date) -> list[PageMetadata]:
        access = "all-access"
        path = f"/pageviews/top/{self.project}/{access}/{date}"
        url = self.url + path

        response = requests.get(url, headers=self.headers)
        data = response.json()

        top_pages = []
        for item in data["items"][0]["articles"]:
            page_name = item["article"]
            view_count = item["views"]
            rank = item["rank"]
            top_pages.append(PageMetadata(page_name, rank, view_count=view_count))

        return top_pages
