from analytics_api.analytics_api import AnalyticsAPI
from wikimedia_api.wikimedia_api import WikimediaApi
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

api = AnalyticsAPI()

top_edits = api.get_most_edited_articles("01", "07", "2024")

pages_to_process = list(map(lambda x: x.name, top_edits[:10]))

for i in range(1, 31):
    day = str(i).zfill(2)
    print(day)
    for page in pages_to_process:
        try:
            view_count = api.get_page_views(page, f"202407{day}", f"202407{day}")
            edit_count = api.get_page_edits(page, f"202407{day}", f"202407{day}")
            print(page, view_count, edit_count)
        except Exception as e:
            # print(e)
            continue
    print("-----------")
