SELECT date, page_name
FROM wikipedia_data.mock_final_table
WHERE date={{date}}
LIMIT {{limit}};
