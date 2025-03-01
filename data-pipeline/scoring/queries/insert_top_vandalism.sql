INSERT INTO wikipedia_data.top_vandalism_final_table
WITH grouped AS (
  SELECT
    page_name,
    CAST(AVG(view_count) AS INT) as view_count,
    CAST(AVG(edit_count) AS INT) as edit_count,
    CAST(AVG(revert_count) AS INT) as revert_count,
    CAST(AVG(editor_count) AS INT) as editor_count,
    CAST(AVG(net_bytes_changed) AS INT) as net_bytes_changed,
    CAST(AVG(abs_bytes_changed) AS INT) as abs_bytes_changed,
    CAST(AVG(abs_bytes_reverted) AS INT) as abs_bytes_reverted
  FROM
    wikipedia_data.intermediate_table
  WHERE
    {{dateSelectionStr}}
  GROUP BY
    page_name
)
(
  SELECT
    CAST({{date}} AS DATE) AS date,
    *,
    revert_count/edit_count AS percent_reverted,
    abs_bytes_reverted/revert_count AS avg_bytes_reverted_per_revert
  FROM
    grouped
  WHERE
    revert_count > 3 and
    view_count > 100 and 
    revert_count/edit_count > 0.7 and
    abs_bytes_reverted/revert_count > 50
  ORDER BY
    revert_count DESC
  LIMIT {{limit}}
)
