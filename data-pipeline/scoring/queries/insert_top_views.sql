INSERT INTO wikipedia_data.top_views_final_table (
    SELECT date, page_name, view_count
    FROM (
        SELECT date, page_name, view_count
        FROM wikipedia_data.intermediate_table
        where date={{date}}
    )
    order by view_count desc
    limit {{limit}}
)