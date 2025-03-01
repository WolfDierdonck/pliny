SELECT
    date,
    page_name,
    view_count,
    edit_count,
    revert_count,
    editor_count,
    net_bytes_changed,
    abs_bytes_changed,
    abs_bytes_reverted
FROM wikipedia_data.top_edits_final_table
WHERE
    date = {{date}}
ORDER BY edit_count DESC
LIMIT {{limit}}
