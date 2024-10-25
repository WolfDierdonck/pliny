class PageRevisionMetadata:
    def __init__(
        self,
        revision_count: int,
        editor_count: int,
        revert_count: int,
        net_bytes_change: int,
    ):
        self.revision_count = revision_count
        self.editor_count = editor_count
        self.revert_count = revert_count
        self.net_bytes_change = net_bytes_change

    def __str__(self) -> str:
        return f"revision_count={self.revision_count}, editor_count={self.editor_count}, revert_count={self.revert_count}, net_bytes_change={self.net_bytes_change}"

    def __repr__(self) -> str:
        return f"PageRevisionMetadata({self})"
