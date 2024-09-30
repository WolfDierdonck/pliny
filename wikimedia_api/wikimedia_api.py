import requests
from typing import Any


class WikimediaApi:
    def __init__(self) -> None:
        self.project = "wikipedia"
        self.language = "en"

        self.url = "https://api.wikimedia.org/core/v1/"

        # ACCESS_TOKEN = os.getenv("WIKIPEDIA_API_ACCESS_TOKEN")
        # self.headers = {
        #     "Authorization": f"Bearer {ACCESS_TOKEN}",
        #     "User-Agent": "pliny_test (wolf.vandierdonck@gmail.com)",
        # }
        self.headers: dict[str, str] = {}

    def get_page_history(self, title: str) -> Any:
        path = f"{self.project}/{self.language}/page/{title}/history"
        url = self.url + path

        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data
