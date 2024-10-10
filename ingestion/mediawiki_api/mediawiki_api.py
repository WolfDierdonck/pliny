import concurrent.futures
from concurrent.futures import Future
import requests

class EndOfPageListException(Exception):
    def __init__(self, final_page_list: list[str]) -> None:
        self.final_page_list = final_page_list

class MediaWikiAPI:
    def __init__(self) -> None:
        self.url = "https://en.wikipedia.org/w/api.php"
        self.headers = {
            "User-Agent": "Pliny test",
            "From": "wolf.vandierdonck@gmail.com",
        }
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
    
    def get_all_pages_starting_from(self, page_name: str) -> Future[tuple[list[str], str]]:
        def fetch_and_process(page_name: str) -> tuple[list[str], str]:
            params = {
                "action": "query",
                "format": "json",
                "list": "allpages",
                "apfrom": page_name,
                "aplimit": "500",
            }
            response = requests.get(self.url, headers=self.headers, params=params)
            data = response.json()

            if "query" not in data or "allpages" not in data["query"]:
                raise ValueError(f"Unexpected response: {data}")

            if "continue" not in data:
                raise EndOfPageListException([page["title"] for page in data["query"]["allpages"]])

            pages = data["query"]["allpages"]
            page_to_continue_from: str = data["continue"]["apcontinue"]
            page_names: list[str] = [page["title"] for page in pages]
            return (page_names, page_to_continue_from)
            
        return self.executor.submit(fetch_and_process, page_name)
