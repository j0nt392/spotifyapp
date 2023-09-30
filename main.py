import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request

# Initialize the Flask app
app = Flask(__name__)

# Define your Spotify API credentials
SPOTIPY_CLIENT_ID = "your api key here"
SPOTIPY_CLIENT_SECRET = "your apip secretkey here"
SPOTIPY_REDIRECT_URI = "redirect uri here"

# Initialize SpotifyOAuth
sp_oauth = SpotifyOAuth(
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    scope="user-library-read user-top-read",
)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    if token_info:
        # Initialize the Spotipy client with the access token
        sp = spotipy.Spotify(auth=token_info['access_token'])
        top_tracks = sp.current_user_top_tracks()
        print("User's Top Tracks:")
        for track in top_tracks['items']:
            print(f"- {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
        return "Authorization successful. You can close this page."
    else:
        return "Authorization failed. Please try again."

if __name__ == '__main__':
    app.run(port=3000)
