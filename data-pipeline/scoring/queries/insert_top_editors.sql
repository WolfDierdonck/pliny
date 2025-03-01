INSERT INTO wikipedia_data.top_editors_final_table
SELECT
    CAST({{date}} AS DATE) AS date,
    *
FROM
    (
        SELECT
            page_name, 
            CAST(AVG(view_count) AS INT) as view_count,
            CAST(AVG(edit_count) AS INT) as edit_count,
            CAST(AVG(revert_count) AS INT) as revert_count,
            CAST(AVG(editor_count) AS INT) as editor_count,
            CAST(AVG(net_bytes_changed) AS INT) as net_bytes_changed,
            CAST(AVG(abs_bytes_changed) AS INT) as abs_bytes_changed,
            CAST(AVG(abs_bytes_reverted) AS INT) as abs_bytes_reverted
        FROM wikipedia_data.intermediate_table
        WHERE
            {{dateSelectionStr}}
        GROUP BY page_name
        ORDER BY editor_count DESC
        LIMIT {{limit}}
    )
