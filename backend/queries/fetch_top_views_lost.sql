SELECT
  date as date,
  page_name,
  current_view_count,
  previous_view_count,
  view_count_ratio
FROM wikipedia_data.top_views_lost_final_table
WHERE date = {{date}}
ORDER BY view_count_ratio asc
limit {{limit}}
