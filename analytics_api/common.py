class PageMetadata:
    def __init__(self, page_name, rank, view_count=None, byte_delta=None):
        self.page_name = page_name
        self.view_count = view_count
        self.rank = rank
        self.byte_delta = byte_delta

