from analytics_api.analytics_api import AnalyticsAPI
from dotenv import load_dotenv
from common.dates import Date, DateRange

load_dotenv(dotenv_path=".env")

start = Date(day=1, month=7, year=2024)
end = Date(day=2, month=7, year=2024)
date_range = DateRange(start, end)

for date in date_range:
    print(date)


# api = AnalyticsAPI()

# top_edits = api.get_most_edited_articles(Date(day=1, month=7, year=2024))

# pages_to_process = list(map(lambda x: x.name, top_edits[:10]))

# for i in range(1, 31):
#     day = Date(day=i, month=7, year=2024)
#     for page in pages_to_process:
#         try:
#             view_count = api.get_page_views(page, day, day)
#             edit_count = api.get_page_edits(page, day, day)
#             print(page, view_count, edit_count)
#         except Exception as e:
#             # print(e)
#             continue
#     print("-----------")
