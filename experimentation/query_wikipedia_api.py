import datetime
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")

today = datetime.datetime.now()
date = today.strftime("%Y/%m/%d")

project = "wikipedia"
language = "en"
title = "Jupiter"
filter_type = "minor"
parameters = {"filter": filter_type}

url = f"https://api.wikimedia.org/core/v1/{project}/{language}/page/{title}/history"

ACCESS_TOKEN = os.getenv("WIKIPEDIA_API_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "User-Agent": "pliny_test (wolf.vandierdonck@gmail.com)",
}

response = requests.get(url)
data = response.json()
print(json.dumps(data, indent=4))
