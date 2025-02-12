SELECT wikipedia_data.top_edits_final_table
SELECT
    CAST({{date}} AS DATE) AS date,
    *
FROM
    (
        SELECT
            page_name, 
            CAST(AVG(edit_count) AS INT) as edit_count
        FROM wikipedia_data.intermediate_table
        WHERE
            {{dateSelectionStr}}
        GROUP BY page_name
        ORDER BY edit_count DESC
        LIMIT {{limit}}
    )
