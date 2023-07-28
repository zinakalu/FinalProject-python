import requests
import os
from dotenv import load_dotenv


load_dotenv()


def get_news(query=None, source=None):
    NEWS_API_KEY = os.getenv("NEWSAPI")
    url = "https://newsapi.org/v2/top-headlines"
    params = {"apiKey": NEWS_API_KEY }

    print(query)

    if query:
        params["q"] = query

    if source:
        params["sources"] = source
    
    print(params)
    
    response = requests.get(url, params=params)
    data = response.json()
    return data