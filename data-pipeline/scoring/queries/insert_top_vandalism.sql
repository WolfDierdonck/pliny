INSERT INTO wikipedia_data.top_vandalism_final_table
WITH grouped AS (
  SELECT
    page_name,
    SUM(view_count) AS view_count,
    SUM(revert_count) AS revert_count,
    SUM(abs_bytes_reverted) AS abs_bytes_reverted,
    SUM(edit_count) AS edit_count
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
    SAFE_DIVIDE(revert_count, edit_count) AS percent_reverted
  FROM
    grouped
  WHERE
    revert_count > 3 and abs_bytes_reverted > 20 and view_count > 100
  ORDER BY
    percent_reverted DESC
  LIMIT {{limit}}
)
