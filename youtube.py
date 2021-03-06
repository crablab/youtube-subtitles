import requests, json, time
from requests_oauthlib import OAuth2Session

class youtube:
    """
    Provides an adaptor to the YouTube API.
    """

    def __init__(self, key, client_id, client_secret):
        self._key = key
        self._id = client_id
        self._secret = client_secret

        # See if we already have a token
        try: 
            f = open("tmp/oauth", "r")
            self._token = json.loads(f.read())
        except IOError:
            # I guess we don't have a file
            self._token = None

    @property
    def _authorization_header(self):
        return {"Authorization": "Bearer {}".format(self._token['access_token'])}

    ## METHODS

    def get_subtitles(self, video_id):
        """
        Orchestrates the download of the subtitle file.

        :param video_id: The YouTube video ID to grab subtitles for
        :returns: URL to the downloaded file
        """

        tracks = self._list_subtitle_tracks(video_id)

        subtitle_files = []

        for track in tracks:
            filename = self._get_track(video_id, track)
            if(filename):
                subtitle_files.append(filename)
        
        return subtitle_files

    def _list_subtitle_tracks(self, video_id):
        """
        Grabs the subtitle tracks (usually just one) for the video. 
        Note: by default this will return the subtitle files in the uploaded language. 

        :param video_id: YouTube video ID to get the tracks for
        :returns: List of subtitle track IDs
        """ 

        r = requests.get("https://www.googleapis.com/youtube/v3/captions/", params={"key": self._key, "videoId": video_id, "part": "id"})

        ids = []
        data = r.json()

        if("items" in data):
            for track in data["items"]:
                ids.append(track["id"])
        
        return ids

    def _get_track(self, video_id, subtitle_id):
        """
        Downloads the subtitle file for a given track. Saved in `tmp` with the format `video_id.track_id`. 
        Requires OAuth (groan) and will initiate that if required.

        :returns: Filename of the subtitle track, False on failure.
        """

        # Get OAuth if needed
        if(not self._check_oauth()):
            self._get_access_token()

        r = requests.get("https://www.googleapis.com/youtube/v3/captions/{}".format(subtitle_id), params={"key": self._key}, headers=self._authorization_header)
        filename = "tmp/{}.{}".format(video_id, subtitle_id)

        if(r.status_code == 200):
            with open(filename, "wb") as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)

            return filename
        else:
            return False

    def _check_oauth(self):
        """
        Checks if an OAuth token was loaded and if it has expired.

        :returns: Boolean success factor
        """

        # Is the property empty
        if(self._token == None):
            return False
        
        # Are the items we need there
        if("access_token" in self._token and "expires_at" in self._token):
            # Has the token expired
            if(self._token['expires_at'] < time.time()):
                return False
        else:
            return False

        return True

    def _get_access_token(self):
        """
        Does all the OAuth magic. 

        Will:
        - Start an OAuth2 session
        - Pass on the auth URL 
        - Take the redirect URL and then grab the token 
        - Set the token in the class and write the JSON to `tmp/oauth` for later

        :returns: Boolean success factor
        """
        scope = ['https://www.googleapis.com/auth/youtube.force-ssl']

        self._oauth = OAuth2Session(self._id, scope=scope, redirect_uri="https://localhost")

        authorization_url, state = self._oauth.authorization_url(
            'https://accounts.google.com/o/oauth2/auth',
            # access_type and prompt are Google specific extra
            # parameters.
            access_type="offline", prompt="select_account")
        
        print('Please go to %s and authorize access.' % authorization_url)
        authorization_response = input('Enter the full callback URL: ')

        self._token = self._oauth.fetch_token(
            'https://accounts.google.com/o/oauth2/token',
            authorization_response=authorization_response,
            # Google specific extra parameter used for client
            # authentication
            client_secret=self._secret)

        # Cache the token so we don't keep having to do this malarky 
        with open("tmp/oauth", "w") as fd:
            fd.write(json.dumps(self._token))

        return True
