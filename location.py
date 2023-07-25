import requests
import os
from dotenv import load_dotenv


load_dotenv()


def get_location():
    location_api_key= os.getenv("LOCATIONAPI")
    response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={location_api_key}')
    data = response.json()


    city = data['city']
    country = data['country_name']
    current_location = f'{city}, {country}'

    return {"current_location": current_location}