INSERT INTO wikipedia_data.top_edits_final_table
SELECT
    CAST({{date}} AS DATE) AS date,
    *,
    abs_bytes_changed / edit_count as avg_bytes_changed_per_edit
FROM
    (
        SELECT
            page_name, 
            CAST(AVG(edit_count) AS INT) as edit_count,
            CAST(AVG(abs_bytes_changed) AS INT) as abs_bytes_changed
        FROM wikipedia_data.intermediate_table
        WHERE {{dateSelectionStr}}
        GROUP BY page_name
    )
WHERE edit_count > 0 AND abs_bytes_changed / edit_count > 100
ORDER BY edit_count DESC
LIMIT {{limit}}
