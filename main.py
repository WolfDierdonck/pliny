from analytics_api.analytics_api import AnalyticsAPI

api = AnalyticsAPI()

data = api.get_most_viewed_articles("01", "07", "2024")
for item in data[:10]:
    print(item.page_name)
