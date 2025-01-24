SELECT page_name as `article`, view_count as `views`
FROM wikipedia_data.intermediate_table_sep
WHERE date="{{date}}"
ORDER BY view_count desc
LIMIT {{limit}};