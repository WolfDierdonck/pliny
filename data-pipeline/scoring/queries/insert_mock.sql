INSERT INTO wikipedia_data.mock_final_table (
    SELECT date, page_name
    FROM (
        SELECT date, page_name
        FROM wikipedia_data.intermediate_table
        where date={{date}}
    )
    limit {{limit}}
)
