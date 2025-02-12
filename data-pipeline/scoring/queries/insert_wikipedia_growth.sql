INSERT INTO wikipedia_data.wikipedia_growth_final_table (
    SELECT 
        date, 
        SUM(net_bytes_changed) AS wikipedia_growth_bytes
    FROM wikipedia_data.intermediate_table
    WHERE
        date = {{date}}
    GROUP BY date
)
