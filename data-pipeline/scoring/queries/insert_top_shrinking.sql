INSERT INTO wikipedia_data.top_shrinking_final_table
SELECT
    CAST({{date}} AS DATE) AS date,
    *
FROM
    (
        SELECT
            page_name, 
            CAST(AVG(net_bytes_changed) AS INT) as net_bytes_changed
        FROM wikipedia_data.intermediate_table
        WHERE
            {{dateSelectionStr}}
        GROUP BY page_name
        ORDER BY net_bytes_changed ASC
        LIMIT {{limit}}
    )
