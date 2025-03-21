SELECT
    date,
    page_name,
    view_count,
    edit_count,
    revert_count,
    editor_count,
    net_bytes_changed,
    abs_bytes_changed,
    abs_bytes_reverted,
    percent_reverted,
    avg_bytes_reverted_per_revert
FROM
    wikipedia_data.top_vandalism_final_table
WHERE
    date = {{date}}
ORDER BY
    revert_count DESC
LIMIT {{limit}}
