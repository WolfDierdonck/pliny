SELECT
    date,
    page_name,
    edit_count
FROM wikipedia_data.top_edits_final_table
WHERE
    date = {{date}}
ORDER BY edit_count DESC
LIMIT {{limit}}
