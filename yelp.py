import requests
import os
import spacy

from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv
# from location import get_location



load_dotenv()

# nlp = spacy.load("en_core_web_sm")  # Loading English language model

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def business_search(search_type, location):
    yelp_api_key = os.getenv("YELPAPI")
    endpoint = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": "bearer %s" % yelp_api_key}
    parameters = {
        'term': search_type,
        'limit': 3,
        'location': location,
        'open_now': True
    }
    response = requests.get(url=endpoint, params=parameters, headers=headers)
    business_data = response.json()

    return business_data['businesses']


def respond_to_yelp_request(question, speak):
    doc = nlp(question)
    location = get_location()
    search_type = None


    for token in doc:
        if token.pos_ == "NOUN":
            search_type = token.text
            break
    

    if location and search_type:
        businesses = business_search(search_type, location)
        speak(f"Here are some {search_type} places in {location}:")
        for business in businesses:
            speak(business['name'])
    else:
        speak("Sorry, I couldn't find any relevant information.")


def get_reviews(business_id_or_alias):
    yelp_api_key = os.getenv("YELPAPI")
    url = f"https://api.yelp.com/v3/businesses/{business_id_or_alias}/reviews"
    headers = {"Authorization": f"Bearer {yelp_api_key}", "accept": "application/json"}
    response = requests.get(url, headers=headers)
    reviews_data = response.json()
    return reviews_data['reviews']