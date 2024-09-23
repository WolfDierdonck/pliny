class PageMetadata:
    def __init__(self, name, rank, view_count=None, byte_delta=None):
        self.name = name
        self.view_count = view_count
        self.rank = rank
        self.byte_delta = byte_delta
