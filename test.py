import os


class RevisionEntry:
    def __init__(self):
        self.page_name = ""
        self.editor_name = ""
        self.comment = ""
        self.text_bytes = 0


class PageRevisionMetadata:
    def __init__(self):
        self.page_name = ""
        self.edit_count = 0
        self.editor_count = 0
        self.revert_count = 0
        self.net_bytes_changed = 0
        self.abs_bytes_changed = 0
        self.abs_bytes_reverted = 0

    def __str__(self) -> str:
        return f"  Page: {self.page_name},\n  Reverts: {self.revert_count},\n  Editors: {self.editor_count},\n  Edits: {self.edit_count},\n  Net Bytes Changed: {self.net_bytes_changed},\n  Abs Bytes Changed: {self.abs_bytes_changed},\n  Abs Bytes Reverted: {self.abs_bytes_reverted}"

    def __repr__(self) -> str:
        return f"PageRevisionMetadata(\n{self}\n)"


INPUT_FILE_PATH = os.path.expanduser(
    "~/Downloads/enwiki-20250303-stubs-meta-hist-incr.xml"
)

# Now, create a file iterator to read the file
file_iterator = open(INPUT_FILE_PATH, "r", encoding="utf-8")

# Read the first 10 lines of the file
aggregated_page_data: dict[str, PageRevisionMetadata] = {}
TEXT = True
while True:
    current_line = ""
    try:
        current_line = next(file_iterator)
    except StopIteration:
        break

    if current_line.startswith("  <page>"):
        PAGE_TITLE = ""
        revision_entries: list[RevisionEntry] = []
        while True:
            inside_page_line = next(file_iterator)
            if inside_page_line.startswith("  </page>"):
                break

            if inside_page_line.startswith("    <title>"):
                PAGE_TITLE = (
                    inside_page_line.replace("<title>", "")
                    .replace("</title>", "")
                    .strip()
                )

            if inside_page_line.startswith("    <revision>"):
                revision_entry = RevisionEntry()
                revision_entry.page_name = PAGE_TITLE
                while True:
                    inside_revision_line = next(file_iterator)
                    if inside_revision_line.startswith("    </revision>"):
                        break

                    if inside_revision_line.startswith("      <contributor>"):
                        while True:
                            inside_contributor_line = next(file_iterator)
                            if inside_contributor_line.startswith(
                                "      </contributor>"
                            ):
                                break

                            if inside_contributor_line.startswith("        <username>"):
                                revision_entry.editor_name = (
                                    inside_contributor_line.replace("<username>", "")
                                    .replace("</username>", "")
                                    .strip()
                                )

                            if inside_contributor_line.startswith("        <ip>"):
                                revision_entry.editor_name = (
                                    inside_contributor_line.replace("<ip>", "")
                                    .replace("</ip>", "")
                                    .strip()
                                )

                    if inside_revision_line.startswith("      <comment>"):
                        revision_entry.comment = (
                            inside_revision_line.replace("<comment>", "")
                            .replace("</comment>", "")
                            .strip()
                            .lower()
                        )

                    if inside_revision_line.startswith("      <text"):
                        revision_entry.text_bytes = int(
                            inside_revision_line.split('bytes="')[1].split('"')[0]
                        )

                revision_entries.append(revision_entry)

        # Now process the page data
        if revision_entries:
            metadata = PageRevisionMetadata()
            metadata.page_name = PAGE_TITLE.replace(" ", "_")
            metadata.edit_count = len(revision_entries)
            metadata.editor_count = len(
                set(revision_entry.editor_name for revision_entry in revision_entries)
            )
            metadata.revert_count = sum(
                "revert" in revision_entry.comment
                for revision_entry in revision_entries
            )

            byte_deltas = []
            for i in range(len(revision_entries) - 1):
                byte_deltas.append(
                    revision_entries[i + 1].text_bytes - revision_entries[i].text_bytes
                )

            metadata.net_bytes_changed = sum(byte_deltas)
            metadata.abs_bytes_changed = sum(abs(delta) for delta in byte_deltas)

            revert_byte_deltas = []
            for i in range(len(revision_entries) - 1):
                if "revert" in revision_entries[i + 1].comment:
                    revert_byte_deltas.append(
                        revision_entries[i + 1].text_bytes
                        - revision_entries[i].text_bytes
                    )

            metadata.abs_bytes_reverted = sum(
                abs(delta) for delta in revert_byte_deltas
            )

            aggregated_page_data[PAGE_TITLE] = metadata

filtered_pages: list[PageRevisionMetadata] = []

for k, v in aggregated_page_data.items():
    if v.revert_count > 0:
        filtered_pages.append(v)

sorted_filtered_pages = list(
    sorted(filtered_pages, key=lambda item: item.revert_count, reverse=True)
)

print(sorted_filtered_pages[:10])
