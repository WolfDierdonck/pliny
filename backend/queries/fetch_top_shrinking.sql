SELECT
    date,
    page_name,
    net_bytes_changed
FROM wikipedia_data.top_shrinking_final_table
WHERE
    date = {{date}}
ORDER BY net_bytes_changed ASC
LIMIT {{limit}}
