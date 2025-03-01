INSERT INTO wikipedia_data.top_views_final_table
select
  t1.date as `date`,
  t1.page_name as `page_name`,
  t1.view_count as `view_count_0`,
  t1.edit_count as `edit_count`,
  t1.revert_count as `revert_count`,
  t1.editor_count as `editor_count`,
  t1.net_bytes_changed as `net_bytes_changed`,
  t1.abs_bytes_changed as `abs_bytes_changed`,
  t1.abs_bytes_reverted as `abs_bytes_reverted`,
  t2.view_count as `view_count_1`,
  t3.view_count as `view_count_2`,
  t4.view_count as `view_count_3`,
  t5.view_count as `view_count_4`,
  t6.view_count as `view_count_5`,
  t7.view_count as `view_count_6`
from wikipedia_data.intermediate_table t1
left join wikipedia_data.intermediate_table t2 on t1.page_name = t2.page_name and t1.date={{date_0}} and t2.date={{date_1}}
left join wikipedia_data.intermediate_table t3 on t1.page_name = t3.page_name and t1.date={{date_0}} and t3.date={{date_2}}
left join wikipedia_data.intermediate_table t4 on t1.page_name = t4.page_name and t1.date={{date_0}} and t4.date={{date_3}}
left join wikipedia_data.intermediate_table t5 on t1.page_name = t5.page_name and t1.date={{date_0}} and t5.date={{date_4}}
left join wikipedia_data.intermediate_table t6 on t1.page_name = t6.page_name and t1.date={{date_0}} and t6.date={{date_5}}
left join wikipedia_data.intermediate_table t7 on t1.page_name = t7.page_name and t1.date={{date_0}} and t7.date={{date_6}}
where t1.date={{date_0}}
order by view_count_0 desc
limit {{limit}}
