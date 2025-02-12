SELECT
    date,
    page_name,
    editor_count
FROM wikipedia_data.top_editors_final_table
WHERE
    date = {{date}}
ORDER BY editor_count DESC
LIMIT {{limit}}
