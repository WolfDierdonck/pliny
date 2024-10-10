from ingestion.mediawiki_api.mediawiki_api import MediaWikiAPI


class MediaWikiPageListIterator:
    def __init__(self, start_char: str) -> None:
        self.cache: list[str] = []
        self.cache_index = 0
        self.current_char = start_char

        self.media_wiki_api = MediaWikiAPI()
        self.fetching_future = self.media_wiki_api.get_all_pages_starting_from(self.current_char)
    
    def __next__(self) -> str:
        # if our cache has been exhausted
        if self.cache_index == len(self.cache):
            # wait for the fetching future to complete and immediately start the next fetch
            future_result = self.fetching_future.result()
            #populate cache
            self.cache = future_result
            #get where to continue from
            #immediately make async request for next batch

            self.fetching_future = self.media_wiki_api.get_all_pages_starting_from(self.current_char)
            


        if (self.cache_index < len(self.cache)):
            self.cache_index += 1
            return self.cache[self.cache_index - 1]
        
        if self.fetching_future is None:
            self.fetching_future = MediaWikiAPI.get_all_pages_starting_from(self.current_char)
        # Otherwise, fetch the next batch
        if self.current_char == "z":
            raise StopIteration
        return selfself.cache[self.cache_index]

class MediaWikiHelper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_all_pages_iterator() -> MediaWikiPageListIterator:
        return MediaWikiPageListIterator("a")
