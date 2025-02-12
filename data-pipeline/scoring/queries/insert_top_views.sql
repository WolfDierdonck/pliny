INSERT INTO wikipedia_data.top_views_final_table
SELECT
    CAST({{date}} AS DATE) AS date,
    *
FROM
    (
        SELECT
            page_name, 
            CAST(AVG(view_count) AS INT) as view_count
        FROM wikipedia_data.intermediate_table
        WHERE
            {{dateSelectionStr}}
        GROUP BY page_name
        ORDER BY view_count DESC
        LIMIT {{limit}}
    )
