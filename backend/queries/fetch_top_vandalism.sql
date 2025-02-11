SELECT
    start_date,
    end_date,
    page_name,
    view_count,
    revert_count,
    bytes_reverted,
    edit_count,
    percent_reverted
FROM
    wikipedia_data.top_vandalism_final_table
WHERE
    start_date = {{startDate}} AND end_date = {{endDate}}
ORDER BY
    percent_reverted DESC
LIMIT {{limit}};
