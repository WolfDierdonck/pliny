from abc import ABC, abstractmethod

from common.dates import Date

from ingestion.wikimedia_dumps.dump_manager import DumpManager

from ingestion.mediawiki_api.mediawiki_helper import MediaWikiPageListIterator

class PageNameDataSource(ABC):
    @abstractmethod
    def get_next_page_name(self) -> str:
        """
        Abstract method to get page names

        Returns:
            page: The next page name
        """
        pass

class PageNameDummy(PageNameDataSource):
    def __init__(self) -> None:
        self.idx = 0
        self.test_pages = ["Earth", "Moon", "Sun", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

    def get_next_page_name(self) -> str:
        if self.idx >= len(self.test_pages):
            raise StopIteration
        page = self.test_pages[self.idx]
        self.idx += 1
        return page

class PageNameWikiMediaAPI(PageNameDataSource):
    def __init__(self) -> None:
        self.iterator = MediaWikiPageListIterator('!') # ! is the first lexigraphical page name

    def get_next_page_name(self) -> str:
        return self.iterator.__next__()

class PageNameDumpFile(PageNameDataSource):
    def __init__(self, date: Date, dump_manager: DumpManager) -> None:
        self.dump_manager = dump_manager
        self.file_name = dump_manager.get_page_view_dump_filename(date)
        self.file = open(self.file_name, 'r')
        self.line_iterator = iter(self.file)
        self.last_line = next(self.line_iterator)

    def get_next_page_name(self) -> str:
        while True:
            split_line = self.last_line.split(" ")
            if (split_line[0] == 'en.wikipedia'
                and not split_line[1].startswith("File:")
                and not split_line[1].startswith("Category:")
                and not split_line[1].startswith("Talk:")):
                
                page_name = split_line[1]
                
                # Lookahead to skip duplicate page names 
                while True:
                    next_line = next(self.line_iterator)
                    split_next_line = next_line.split(" ")
                    if split_next_line[1] != page_name:
                        self.last_line = next_line
                        break
                
                return page_name
            
            elif self.last_line.startswith('en.wikiquote'):
                raise StopIteration # This is immediate stop, as we are not interested in anything other than wikipedia pages

            else:
                self.last_line = next(self.line_iterator)
