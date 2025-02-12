SELECT
    date,
    wikipedia_growth_bytes
FROM wikipedia_data.wikipedia_growth_final_table
WHERE
    date = {{date}}