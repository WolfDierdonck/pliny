from dotenv import load_dotenv
from sql.wikipedia_data_accessor import WikipediaDataAccessor

from google.cloud import bigquery
from google.cloud.bigquery.table import Table
from google.cloud.bigquery.schema import SchemaField

load_dotenv(dotenv_path=".env")

wikipedia_data_accessor = WikipediaDataAccessor("PLINY_BIGQUERY_SERVICE_ACCOUNT", buffer_size=1)
# wikipedia_data_accessor.delete_table("TEST")
# # create the table
# t = wikipedia_data_accessor.create_table("TEST", [
#     bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
#     bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
# ], "age")

# # generate 10000 random rows of random names, age between 1 and 10
# rows = [
#     {"name": f"name_{i}", "age": i % 10 + 1}
#     for i in range(10000)
# ]
# wikipedia_data_accessor.write_to_table(t, rows, False)


# insert a row into TEST
t = wikipedia_data_accessor.get_table("TEST")
wikipedia_data_accessor.write_to_table(t, [{"name": "Wolf", "age": 1}], False)