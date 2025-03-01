SELECT
    date,
    page_name,
    view_count_0,
    edit_count,
    revert_count,
    editor_count,
    net_bytes_changed,
    abs_bytes_changed,
    abs_bytes_reverted,
    view_count_1,
    view_count_2,
    view_count_3,
    view_count_4,
    view_count_5,
    view_count_6
FROM wikipedia_data.top_views_final_table
WHERE
    date = {{date}}
ORDER BY view_count DESC
LIMIT {{limit}}
