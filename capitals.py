import requests
import json
from news import get_news


def handle_query(query):
    
    country_n = query.split(' ')[-1]
    result = get_country_info(country_n)
    print(country_n)
    
    if result is not None:
        print('🙄 please work',result)
        return { 'result': result, 'query': query }
    else:
        return get_news(query)


def get_country_info(country_name):
    response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}?fields=name,capital,population,flags,currencies,languages")

    if response.status_code == 200:
        data = response.json()[0]
        return {
            "name": data["name"]["common"],
            "capital": data["capital"][0] if data["capital"] else "N/A",
            "population": data["population"],
            "flag": data["flags"]["png"],
            "currencies": list(data["currencies"].keys()),
            "languages": list(data["languages"].values())
        }
    else:
        return None


# info = get_country_info("Nigeria")
# print(info)
