from dotenv import load_dotenv, find_dotenv
from youtube import youtube
from subtitle import subtitle
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

#subtitles = yt.get_subtitles(url)

subtitles = ["tmp/D8-8r0wNgiY.l5s234BevlVgiCy9mXQHACIa8X5w8gZkfc67osYzd0o="]

for file in subtitles:
    st = subtitle(file)
    print(st.get_all_text())