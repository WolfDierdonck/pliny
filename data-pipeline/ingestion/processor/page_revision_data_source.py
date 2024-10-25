from abc import ABC, abstractmethod
from concurrent.futures import Future

from common.dates import Date
from common.page_revision_metadata import PageRevisionMetadata
from ingestion.mediawiki_api.mediawiki_api import MediaWikiAPI


class PageRevisionDataSource(ABC):
    @abstractmethod
    def get_page_revision_metadata(
        self, page: str, date: Date
    ) -> Future[PageRevisionMetadata]:
        """
        Abstract method to get page revision metadata.

        Args:
            page (str): The page to get revision metadata for.
            date (datetime): The date to get revision metadata for.

        Returns:
            dict: The revision metadata for the page.
        """
        pass


class PageRevisionAPI(PageRevisionDataSource):
    def __init__(self) -> None:
        self.media_wiki_api = MediaWikiAPI()

    def get_page_revision_metadata(
        self, page: str, date: Date
    ) -> Future[PageRevisionMetadata]:
        return self.media_wiki_api.get_page_revision_metadata(page, date)
