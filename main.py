from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlparse, parse_qsl
from youtube import youtube
from subtitle import subtitle
from dumb_analyzer import dumb_analyzer
import os

# Setup the YouTube class
load_dotenv(find_dotenv())
youtube_key = os.getenv("YOUTUBE_KEY")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
yt = youtube(youtube_key, client_id, client_secret)

print("=== The YouTube Subtitle Game ===")
print("Enter video ID at prompt, null for finished")

# TODO: strip ID from the URL

subtitles = []

while True:
    url = input("> ")
    
    if(url):
        up = urlparse(url)
        params = parse_qsl(up.query)
        if("v" in params[0]):
            subtitles.extend(yt.get_subtitles(params[0][1]))
        else:
            print("Not a valid YouTube URL")
            continue
    else:
        break

phrases = []

for file in subtitles:
    # Get the file
    st = subtitle(file)
    string = st.get_all_text()

    # Calculate the frequencies 
    fq = dumb_analyzer()
    local_phrases = fq.most_frequent_phrases(string)

    phrases.extend(local_phrases)

# Sort the phrases again by frequency, across all videos
for item in sorted(phrases, key=lambda x: x[1], reverse=True):
    print(item)