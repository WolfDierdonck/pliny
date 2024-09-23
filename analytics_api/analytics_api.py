import requests
from analytics_api.common import PageView


class AnalyticsAPI:
    def __init__(self):
        self.project = "en.wikipedia.org"
        self.url = "https://wikimedia.org/api/rest_v1/metrics"

    def get_most_viewed_articles(self, day, month, year):
        access = "all-access"
        path = f"/pageviews/top/{self.project}/{access}/{year}/{month}/{day}"
        url = self.url + path

        headers = {
            "User-Agent": "Pliny test",
            "From": "wolf.vandierdonck@gmail.com",
        }

        print(url)
        response = requests.get(url, headers=headers)
        data = response.json()

        top_pages = []
        for item in data["items"][0]["articles"]:
            page_name = item["article"]
            view_count = item["views"]
            rank = item["rank"]
            top_pages.append(PageView(page_name, view_count, rank))

        return top_pages
