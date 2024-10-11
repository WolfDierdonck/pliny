from ingestion.mediawiki_api.mediawiki_api import  MediaWikiAPI


class MediaWikiPageListIterator:
    def __init__(self, start_page: str) -> None:
        self.cache: list[str] = []
        self.cache_index = 0
        self.page_to_fetch: str | None = start_page

        self.media_wiki_api = MediaWikiAPI()
        self.fetching_future = self.media_wiki_api.get_all_pages_starting_from(self.page_to_fetch)
    
    def __next__(self) -> str:
        # if our cache has been exhausted, wait for fetching future and fetch next batch
        if self.cache_index == len(self.cache):
            if self.page_to_fetch == None:       #cache empty and no new future
                raise StopIteration

            self.cache_index = 0
            future_result = self.fetching_future.result()
            #populate cache
            self.cache = future_result[0]
            #get where to continue from
            self.page_to_fetch = future_result[1]
            #immediately make async request for next batch
            if self.page_to_fetch is not None:
                self.fetching_future = self.media_wiki_api.get_all_pages_starting_from(self.page_to_fetch)

        # return next page from cache
        cached_page = self.cache[self.cache_index]
        self.cache_index += 1
        return cached_page

class MediaWikiHelper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_all_pages_iterator() -> MediaWikiPageListIterator:
        return MediaWikiPageListIterator("!")
