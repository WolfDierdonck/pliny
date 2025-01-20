class PageRevisionMetadata:
    def __init__(
        self,
        edit_count: int,
        editor_count: int,
        revert_count: int,
        total_bytes_changed: int,
        total_bytes_reverted: int,
    ):
        self.edit_count = edit_count
        self.editor_count = editor_count
        self.revert_count = revert_count
        self.total_bytes_changed = total_bytes_changed
        self.total_bytes_reverted = total_bytes_reverted

    def __str__(self) -> str:
        return f"edit_count={self.edit_count}, editor_count={self.editor_count}, revert_count={self.revert_count}, total_bytes_changed={self.total_bytes_changed}, total_bytes_reverted={self.total_bytes_reverted}"

    def __repr__(self) -> str:
        return f"PageRevisionMetadata({self})"
