SELECT date, page_name, view_count
FROM wikipedia_data.top_views_final_table
WHERE date={{date}}
ORDER BY view_count desc
LIMIT {{limit}};
