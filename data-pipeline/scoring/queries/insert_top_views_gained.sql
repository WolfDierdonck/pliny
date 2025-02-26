INSERT INTO wikipedia_data.top_views_gained_final_table
SELECT 
  today.date as date,
  today.page_name as page_name,
  today.view_count as current_view_count,
  yesterday.view_count as previous_view_count,
  today.view_count / yesterday.view_count as view_count_ratio
FROM wikipedia_data.intermediate_table today
inner join wikipedia_data.intermediate_table yesterday
on today.page_name = yesterday.page_name and today.date = {{todayDate}} and yesterday.date = {{yesterdayDate}}
WHERE today.view_count > 10000 and yesterday.view_count > 10000
ORDER BY view_count_ratio desc
limit {{limit}}
