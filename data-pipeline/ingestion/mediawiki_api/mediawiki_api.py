import concurrent.futures
from concurrent.futures import Future
import requests


class MediaWikiAPI:
    def __init__(self) -> None:
        self.url = "https://en.wikipedia.org/w/api.php"
        self.headers = {
            "User-Agent": "Pliny test",
            "From": "wolf.vandierdonck@gmail.com",
        }
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)

    def get_all_pages_starting_from(
        self, page_name: str
    ) -> Future[tuple[list[str], str | None]]:
        def fetch_and_process(page_name: str) -> tuple[list[str], str | None]:
            # filter out redirects as many symbols redirect to pages we've already seen; ⬢ redirects to Hexagon
            # redirects also result in 404 when querying for edit count on wikimedia analytics api
            params = {
                "action": "query",
                "format": "json",
                "list": "allpages",
                "apfilterredir": "nonredirects",
                "apfrom": page_name,
                "aplimit": "500",
            }
            response = requests.get(self.url, headers=self.headers, params=params)
            data = response.json()

            if "query" not in data or "allpages" not in data["query"]:
                raise ValueError(f"Unexpected response: {data}")

            pages = data["query"]["allpages"]
            page_names: list[str] = [page["title"] for page in pages]

            page_to_continue_from = None
            if "continue" in data and "apcontinue" in data["continue"]:
                page_to_continue_from = data["continue"]["apcontinue"]

            return (page_names, page_to_continue_from)

        return self.executor.submit(fetch_and_process, page_name)
