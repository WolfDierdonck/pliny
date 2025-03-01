SELECT
  date as date,
  page_name,
  current_view_count,
  one_day_ago_view_count,
  two_days_ago_view_count,
  view_count_ratio
FROM wikipedia_data.top_views_lost_final_table
WHERE date = {{date}}
ORDER BY view_count_ratio asc
limit {{limit}}
