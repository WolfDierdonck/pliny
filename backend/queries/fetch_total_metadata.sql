SELECT
    date,
    total_edit_count,
    total_view_count,
    total_editor_count,
    total_revert_count,
    total_net_bytes_changed
FROM wikipedia_data.total_metadata_final_table
WHERE
    date = {{date}}
