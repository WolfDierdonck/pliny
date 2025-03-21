class PageRevisionMetadata:
    def __init__(
        self,
        edit_count: int,
        editor_count: int,
        revert_count: int,
        net_bytes_changed: int,
        abs_bytes_changed: int,
        abs_bytes_reverted: int,
    ):
        self.edit_count = edit_count
        self.editor_count = editor_count
        self.revert_count = revert_count
        self.net_bytes_changed = net_bytes_changed
        self.abs_bytes_changed = abs_bytes_changed
        self.abs_bytes_reverted = abs_bytes_reverted

    def __str__(self) -> str:
        return f"edit_count={self.edit_count}, editor_count={self.editor_count}, revert_count={self.revert_count}, net_bytes_changed={self.net_bytes_changed}, abs_bytes_changed={self.abs_bytes_changed}, abs_bytes_reverted={self.abs_bytes_reverted}"

    def __repr__(self) -> str:
        return f"PageRevisionMetadata({self})"
