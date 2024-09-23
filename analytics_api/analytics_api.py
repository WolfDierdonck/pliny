import requests
from analytics_api.common import PageMetadata


class AnalyticsAPI:
    def __init__(self):
        self.project = "en.wikipedia.org"
        self.url = "https://wikimedia.org/api/rest_v1/metrics"
        self.headers = {
            "User-Agent": "Pliny test",
            "From": "wolf.vandierdonck@gmail.com",
        }

    def get_most_edited_articles(self, day, month, year):
        editor_type = "user"
        page_type = "content"
        path = f"/edited-pages/top-by-net-bytes-difference/{self.project}/{editor_type}/{page_type}/{year}/{month}/{day}"
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

    def get_most_viewed_articles(self, day, month, year):
        access = "all-access"
        path = f"/pageviews/top/{self.project}/{access}/{year}/{month}/{day}"
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
