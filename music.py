import spotipy
import time
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
api_key = os.getenv("MUSICAPI")

def search_song(api_key, song):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=song,
        part='id, snippet',
        maxResults=1
    )

    response = request.execute()

    print(response)

    if response['items']:
        return response['items'][0]['id']['videoId']

    else:
        return None

search_song(api_key, "Firework")
