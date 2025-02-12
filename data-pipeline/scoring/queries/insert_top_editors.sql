INSERT INTO wikipedia_data.top_editors_final_table
SELECT
    CAST({{date}} AS DATE) AS date,
    *
FROM
    (
        SELECT
            page_name, 
            CAST(AVG(editor_count) AS INT) as editor_count
        FROM wikipedia_data.intermediate_table
        WHERE
            {{dateSelectionStr}}
        GROUP BY page_name
        ORDER BY editor_count DESC
        LIMIT {{limit}}
    )
