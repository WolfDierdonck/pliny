INSERT INTO wikipedia_data.total_metadata_final_table (
    SELECT 
        date, 
        SUM(edit_count) AS total_edit_count,
        SUM(view_count) AS total_view_count,
        SUM(editor_count) AS total_editor_count,
        SUM(revert_count) AS total_revert_count,
        SUM(net_bytes_changed) AS total_net_bytes_changed
    FROM wikipedia_data.intermediate_table
    WHERE
        date = {{date}}
    GROUP BY date
)
