INSERT INTO wikipedia_data.top_vandalism_final_table
WITH grouped AS (
  SELECT
    CAST({{startDate}} AS DATE) start_date,
    CAST({{endDate}} AS DATE) AS end_date,
    page_name,
    SUM(view_count) AS view_count,
    SUM(revert_count) AS revert_count,
    SUM(total_bytes_reverted) AS bytes_reverted,
    SUM(edit_count) AS edit_count
  FROM
    `wikipedia_data.intermediate_table`
  WHERE
    date >= {{startDate}}
    AND date <= {{endDate}}
  GROUP BY
    page_name
)
(
  SELECT
    *,
    SAFE_DIVIDE(revert_count, edit_count) AS percent_reverted
  FROM
    grouped
  WHERE
    revert_count > 25 and bytes_reverted > 100 and view_count > 1000
  ORDER BY
    percent_reverted DESC
  LIMIT {{limit}}
)
