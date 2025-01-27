INSERT INTO wikipedia_data.top_views_final_table (
    SELECT date, page_name as 'article', view_count as 'views'
    FROM (
        SELECT date, page_name, view_count
        FROM wikipedia_data.intermediate_table_sep
        where date={{date}}
    )
    order by views desc
    limit {{limit}}
)