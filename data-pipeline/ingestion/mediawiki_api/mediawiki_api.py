import concurrent.futures
from concurrent.futures import Future
import requests

from common.dates import Date
from common.page_revision_metadata import PageRevisionMetadata


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

    def get_page_revision_metadata(
        self, page_name: str, date: Date
    ) -> Future[PageRevisionMetadata]:
        def fetch_and_process(
            page_name: str, continue_from: str | None
        ) -> tuple[list[dict], str | None]:
            start_timestamp = date.to_py_date().isoformat() + "T00:00:00Z"
            end_timestamp = date.add_days(1).to_py_date().isoformat() + "T00:00:00Z"

            params = {
                "action": "query",
                "format": "json",
                "prop": "revisions",
                "titles": page_name,
                "rvprop": "timestamp|user|tags|size",
                "rvstart": start_timestamp,
                "rvend": end_timestamp,
                "rvdir": "newer",
                "rvlimit": "500",
            }
            if continue_from is not None:
                params["rvcontinue"] = continue_from

            response = requests.get(self.url, headers=self.headers, params=params)

            try:
                data = response.json()
            except Exception as _:
                raise ValueError(f"Could not parse response: {response.text}")

            result_continue_from: str | None = None
            if "continue" in data and "rvcontinue" in data["continue"]:
                result_continue_from = data["continue"]["rvcontinue"]

            if "query" not in data or "pages" not in data["query"]:
                raise ValueError(f"Unexpected response: {data}")

            pages = data["query"]["pages"]

            page_data = next(iter(pages.values()))

            if "revisions" not in page_data:
                return [], result_continue_from

            revisions = page_data["revisions"]
            return revisions, result_continue_from

        def helper_loop(page_name: str) -> PageRevisionMetadata:
            revisions = []
            first_page_revisions, continue_from = fetch_and_process(page_name, None)
            revisions.extend(first_page_revisions)

            while continue_from is not None:
                next_page_revisions, continue_from = fetch_and_process(
                    page_name, continue_from
                )
                revisions.extend(next_page_revisions)

            # Process revisions into three integers
            edit_count = len(revisions)
            editor_count = len(set(revision["user"] for revision in revisions))
            revert_count = sum(
                "mw-reverted" in revision["tags"] for revision in revisions
            )

            # FIXME: This doesn't compute the delta of the first revision, since it doesn't have a previous revision to compare to
            byte_deltas = []
            for i in range(len(revisions) - 1):
                byte_deltas.append(
                    revisions[i + 1]["size"] - revisions[i]["size"]
                )

            net_bytes_changed = sum(byte_deltas)
            abs_bytes_changed = sum(abs(delta) for delta in byte_deltas)

            revision_byte_deltas = []
            for i in range(len(revisions)):
                if "mw-reverted" in revisions[i + 1]["tags"]:
                    revision_byte_deltas.append(
                        revisions[i + 1]["size"] - revisions[i]["size"]
                    )
                
            abs_bytes_reverted = sum(abs(delta) for delta in revision_byte_deltas)

            return PageRevisionMetadata(
                edit_count=edit_count,
                editor_count=editor_count,
                revert_count=revert_count,
                net_bytes_changed=net_bytes_changed,
                abs_bytes_changed=abs_bytes_changed,
                abs_bytes_reverted=abs_bytes_reverted,
            )

        return self.executor.submit(helper_loop, page_name)
