SELECT
    date,
    total_edit_count,
    total_view_count,
    total_editor_count,
    total_revert_count
FROM wikipedia_data.total_metadata_final_table
WHERE
    date = {{date}}
