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
from translate import translate_text
from email_sender import send_questions_email
from database import db
from flask_migrate import Migrate
from models import User, Question



load_dotenv()

app = Flask(__name__)
CORS(app,origins=["http://localhost:3000"])

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
migrate= Migrate(app,db)
db.init_app(app)

# SENDGRID_API_KEY = os.getenv("email_key")
NEWS_API_KEY = os.getenv("NEWSAPI")
yelp_api_key = os.getenv("YELPAPI")

# @app.post('/save-question')
# def save_question():
#     data = request.json
#     question_content = data.get('question')
#     username = data.get('username')
#     email = data.get('email')
#     print(email)

#     user = User.query.filter_by(email=email).first()
#     if not user:
#         user = User(username=username, email=email)
#         db.session.add(user)
#         db.session.commit()

#     new_question = Question(content=question_content, user=user)
#     user.questions.append(new_question)

#     db.session.add(new_question)
#     db.session.commit()

#     return jsonify({"message": "Quuestion saved successfully"}), 201


# @app.get('/get-questions')
# def get_questions():
#     email = request.args.get('email')
#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return jsonify({"error": "User not found!"}), 400

#     questions = [q.content for q in user.questions]
#     return jsonify({"questions": questions}), 200

@app.post('/send-email')
def send_email():
    data = request.get_json()
    email = data['email']
    questions = data['questions']
    print(questions)

    email_sender = 'pythontestingphase3@gmail.com'
    email_password = os.getenv("email_key")

    try:
        send_questions_email(email_sender, email_password, email, questions)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post('/translate')
def translate_text_route():
    data = request.get_json()
    text = data.get('text')
    target = data.get('target')
    print('😏workkkk',target)


    if text and target:
        translated_text = translate_text(text, target)
        print('🤞🏾🤞🏾', translated_text)
        return jsonify({'translatedText': translated_text})

    else:
        return jsonify({'error': 'Invalid input'}), 400
    

@app.get('/country_info')
def country_info():
    country = request.args.get('country')
    info = get_country_info(country)
    print(info)

    return jsonify({'country_info': info})


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
    sources = request.args.get('sources')
    news_data = handle_query(sources)
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