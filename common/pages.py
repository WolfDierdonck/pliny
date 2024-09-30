from typing import Optional


class PageMetadata:
    def __init__(
        self,
        name: str,
        rank: int,
        view_count: Optional[int] = None,
        byte_delta: Optional[int] = None,
    ):
        self.name = name
        self.view_count = view_count
        self.rank = rank
        self.byte_delta = byte_delta
