from analytics_api.analytics_api import AnalyticsAPI
from wikimedia_api.wikimedia_api import WikimediaApi
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

api = AnalyticsAPI()

data = api.get_most_edited_articles("01", "07", "2024")
for item in data[:10]:
    print(item.page_name)
