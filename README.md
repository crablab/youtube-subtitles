# youtube-subtitles

A Python CLI application which will extract the most common phrases from video subtitles, and present them to you. 

Probably most useful as an amusing game. 

## Installation

Requires:

- Python3

Try running it, if you're missing any packages then just install them with `pip`. Apologies for no `pipenv`. 

Setup: 

Create a `.env` in the repository root with the following values:
```
YOUTUBE_KEY={Your YouTube API key}
CLIENT_ID={Your YouTube OAuth2 Client ID}
CLIENT_SECRET={Your YouTube OAuth2 Client Secret}
```

Note: the permissions scope required is `https://www.googleapis.com/auth/youtube.force-ssl` 

## Useage 

Run with `python3 main.py`. 

Copy and paste URLs to YouTube videos. Supply a null value to perform the analysis.

Try to include as many of the outputted phrases as possible, in normal conversation. 

## Future

This was a Sunday afternoon project - don't expect miracles. 

I might: 
- Fix bugs/Issues 
- Accept PRs
- Host this somewhere with a nice UI 
