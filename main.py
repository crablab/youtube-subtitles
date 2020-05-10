from dotenv import load_dotenv, find_dotenv
from youtube import youtube
import os

# Setup the YouTube class
load_dotenv(find_dotenv())
youtube_key = os.getenv("YOUTUBE_KEY")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
yt = youtube(youtube_key, client_id, client_secret)

print("=== The YouTube Subtitle Game ===")

#url = input("Enter video ID: ") # TODO: strip from the URL

url = "D8-8r0wNgiY"

yt.get_subtitles(url)