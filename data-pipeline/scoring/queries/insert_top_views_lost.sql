INSERT INTO wikipedia_data.top_views_lost_final_table
SELECT 
  today.date as date,
  today.page_name as page_name,
  today.view_count as current_view_count,
  yesterday.view_count as one_day_ago_view_count,
  two_days_ago.view_count as two_days_ago_view_count,
  IF(yesterday.view_count is null, 
    cast('inf' as float64), 
    today.view_count / yesterday.view_count
  ) as view_count_ratio
FROM wikipedia_data.intermediate_table today
left join wikipedia_data.intermediate_table yesterday
on today.page_name = yesterday.page_name and today.date = {{todayDate}} and yesterday.date = {{yesterdayDate}}
left join wikipedia_data.intermediate_table two_days_ago
on today.page_name = two_days_ago.page_name and today.date = {{todayDate}} and two_days_ago.date = {{twoDaysAgoDate}}
WHERE yesterday.view_count > 10000 and today.date = {{todayDate}}
ORDER BY view_count_ratio asc, current_view_count asc
limit {{limit}}
