from flask import Flask, request, jsonify, url_for, session, redirect
from flask_cors import CORS
from listen_and_respond import listen_and_respond
from weather import get_weather
from ask_gpt3 import ask_gpt3
import location
import os
import secrets
from music import search_song
import yelp
import requests
from news import get_news
from dotenv import load_dotenv
from requests_html import HTMLSession
from capitals import get_country_info, handle_query


load_dotenv()

app = Flask(__name__)
CORS(app)



NEWS_API_KEY = os.getenv("NEWSAPI")
yelp_api_key = os.getenv("YELPAPI")



# @app.get('/get-username')
# data = request.

@app.get('/country_info')
def country_info():
    country = request.args.get('country')
    info = get_country_info(country)
    print(info)

    return jsonify({'country_info': info})

# @app.post('/get_recipe')
# def get_recipe():
#     data = request.get_json()  # get data from POST request

#     url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"

#     headers = {
#         "X-RapidAPI-Key": "YOUR_SPOONACULAR_API_KEY",
#         "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params=data)

#     return jsonify(response.json())



@app.post('/song')
def create_song():
    data = request.get_json()
    song = data
    print(f"THIS IS THE DATA: {data}")
    api_key = os.getenv("MUSICAPI")
    video_id = search_song(api_key, song)

    return jsonify({'video_id': video_id})


#Weather
@app.get('/get-weather')
def get_weather_route():
    city = request.args.get('city')
    print(city)
    weather_info = get_weather(city)

    return jsonify({'weather_info': weather_info})


@app.get('/ask-gpt3')
def get_answers_from_gpt3():
    question = request.args.get('question')
    response = ask_gpt3(question)
    return jsonify({'response': response})


@app.get('/get-location')
def get_location():
    current_location = location.get_location()
    return jsonify({"current_location": current_location})


@app.get('/get-news')
def get_news_route():
    
    print('💞',request.args)
    sources = request.args.get('sources')
    news_data = handle_query(sources)
    # news_data = get_news(sources)
    url = f"https://newsapi.org/v2/top-headlines?apiKey={NEWS_API_KEY}&sources={sources}"
    return jsonify(news_data)


#YELP
@app.get('/search-business')
def search_business():
    search_type = request.args.get('search_type')
    location = request.args.get('location')

    businesses = yelp.business_search(search_type, location)

    return jsonify(businesses)

@app.get('/get-reviews')
def get_reviews():
    business_id_or_alias = request.args.get('business_id_or_alias')
    headers = {"Authorization": f"Bearer {yelp_api_key}"}

    url = f"https://api.yelp.com/v3/businesses/{business_id_or_alias}/reviews"
    
    response = requests.get(url, headers=headers)
    review_data = response.json()

    return jsonify(review_data)




if __name__ == "__main__":
    app.run(port=5555, debug=True)