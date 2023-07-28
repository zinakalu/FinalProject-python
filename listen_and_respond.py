import speech_recognition as sr
import nltk
import os
import ask_gpt3
import requests


from nltk.corpus import stopwords
from gtts import gTTS
from playsound import playsound
from news import get_news
from weather import kelvin_to_celsius_fahrenheit, get_weather
from location import get_location


nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

r = sr.Recognizer()

def get_keywords(text):
    words = nltk.word_tokenize(text)
    keywords = [word for word in words if word not in stop_words]
    return keywords


def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)



def listen_and_respond():
    with sr.Microphone() as source:
        speak("Talk")
        audio_text = r.listen(source)
    
    try:
        recognized_text = r.recognize_google(audio_text)
        print("Recognized Text:", recognized_text)

        question = recognized_text.lower()

        if "weather" in question:
            respond_to_weather_request(question)

        elif "news" in question:
            respond_to_news_request(question)

        elif "restaurant" in question or "food" in question or "to eat" in question or "eat" in question or "drink" in question or "restaurants" in question:
            restaurant_name = extract_restaurant_name(question)
            if restaurant_name and location:
                speak(f"Getting reviews for {restaurant_name}.")
                get_reviews_for_restaurant(restaurant_name, location)
            else:
                speak("Sorry, I couldn't understand the restaurant name.")

        elif "where am I" in question or "what is my current location" in question or "location" in question:
            current_location = get_location()["current_location"]
            speak(f"Your current location is {current_location}.")

        elif "play" in question:
            song_name = extract_song_name(question)
        
        elif "download" in question:
            song_name = extract_song_name(question)

        else:
            respond_to_general_request(question)

    except sr.UnknownValueError:
        print("Speech Recongition could not understand audio")

def respond_to_weather_request(question):
    city = question.split("in")[-1].strip()
    #Call the Flask API to get the weather
    response = requests.get('http://localhost:5555/get-weather', params={'city': city})
    print(response.text)
    weather_info = response.json().get('weather_info')
    speak(weather_info)


def respond_to_news_request(question):
    topic = None

    if "sports" in question:
        topic = "sports"
    elif "news" in question:
        topic = "news"
    

    if topic:
        news_data = get_news(topic)

        if news_data["totalResults"] > 0:
            articles = news_data["articles"]
            speak(f"Here are the top 3 news articles related to your question:")
            for i, article in enumerate(articles[:3], start=1):
                speak(f"News {i}: {article['title']}")
        else:
            speak(f"There are no news articles about {topic} today.")

    else:
        speak("I'm sorry, I currently don't have news information available for that topic.")

        

def respond_to_general_request(question):
    response = ask_gpt3.ask_gpt3(question)
    speak(response)


def extract_restaurant_name(text):
    review_keywords = ["restaurant", "food", "eat", "drink", "restaurants"]

    words = nltk.word_tokenize(text.lower())

    keyword_index = None
    for i, word in enumerate(words):
        if word in review_keywords:
            keyword_index = i
            break

    if keyword_index is None:
        return None

    restaurant_name = " ".join(words[keyword_index + 1:])

    return restaurant_name.strip()


def get_reviews_for_restaurant(restaurant_name, location):
    businesses = yelp.business_search(restaurant_name, location)

    if businesses:
        # Getting reviews for the first matching restaurant
        business_id_or_alias = businesses[0]['id']
        response = requests.get(f"http://localhost:5555/get-reviews?business_id_or_alias={business_id_or_alias}")
        review_data = response.json()

        if 'reviews' in review_data:
            reviews = review_data['reviews']
            if reviews:
                speak(f"Here are some reviews for {restaurant_name} in {location}:")
                for review in reviews:
                    speak(review['text'])
            else:
                speak(f"Sorry, there are no reviews available for {restaurant_name} in {location}.")
        else:
            speak(f"Sorry, no reviews were found for {restaurant_name} in {location}.")
    else:
        speak(f"Sorry, I couldn't find any information about {restaurant_name} in {location}.")

# listen_and_respond()