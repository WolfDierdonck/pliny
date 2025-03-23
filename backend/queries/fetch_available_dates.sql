SELECT PARSE_DATE('%Y%m%d', partition_id) as date FROM wikipedia_data.INFORMATION_SCHEMA.PARTITIONS
WHERE table_name = 'total_metadata_final_table'
ORDER BY date ASC
