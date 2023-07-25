import requests
import json
import datetime as dt
# from dotenv import load_dotenv
# import os




# load_dotenv()
# print(os.getenv('WEATHERAPI'))


def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit


# print(response)

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    weather_api_key = "11a9a5df58687911039ff94b9f8cb010"

    url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get(url).json()
    # print(response)
    forecast = response['list'][0]
    temp_kelvin = forecast['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
    feels_like_kelvin = forecast['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
    description = forecast['weather'][0]['description']

    weather_info = (f"Temperature in {city}: {temp_celsius:.0f}°C or if you're American {temp_fahrenheit:.0f}°F "
                    f"It feels like: {feels_like_fahrenheit:.0f}°F " #these two lines this and below don't work yet
                    f"General Weather in {city} is: {description}"
    )
    return weather_info