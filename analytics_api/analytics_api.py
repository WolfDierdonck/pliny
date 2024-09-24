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

    def get_page_views(self, page_name, start_date, end_date):
        access = "all-access"
        agent = "all-agents"
        granularity = "daily"
        path = f"/pageviews/per-article/{self.project}/{access}/{agent}/{page_name}/{granularity}/{start_date}/{end_date}"
        url = self.url + path
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data["items"][0]["views"]
    
    def get_page_edits(self, page_name, start_date, end_date):
        editor_type = "user"
        granularity = "daily"
        path = f"/bytes-difference/net/per-page/{self.project}/{page_name}/{editor_type}/{granularity}/{start_date}/{end_date}"
        url = self.url + path
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data["items"][0]["results"][0]["net_bytes_diff"]
        

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
