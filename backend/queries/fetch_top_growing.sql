SELECT
    date,
    page_name, 
    net_bytes_changed,
FROM wikipedia_data.top_growing_final_table
WHERE date = {{date}}
ORDER BY net_bytes_changed DESC
LIMIT {{limit}}
