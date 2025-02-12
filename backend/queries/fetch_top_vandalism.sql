SELECT
    date,
    page_name,
    view_count,
    revert_count,
    abs_bytes_reverted,
    edit_count,
    percent_reverted
FROM
    wikipedia_data.top_vandalism_final_table
WHERE
    date = {{date}}
ORDER BY
    percent_reverted DESC
LIMIT {{limit}}
