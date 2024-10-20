import requests
from typing import Any
import concurrent.futures
from concurrent.futures import Future


class WikiMediaApi:
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
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)

    def get_page_history(self, title: str) -> Future[tuple[str, Any]]:
        def fetch_and_process(title: str) -> tuple[str, Any]:
            path = f"{self.project}/{self.language}/page/{title}/history"
            url = self.url + path

            response = requests.get(url, headers=self.headers)
            data = response.json()

            return title, data

        return self.executor.submit(fetch_and_process, title)
