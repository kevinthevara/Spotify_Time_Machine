import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

URL_ENDPOINT = "https://www.billboard.com/charts/hot-100/"
SPOTIFY_CLIENT_ID = "SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "SPOTFY_CLIENT_SECRET"
REDIRECT_URI = "http://example.com"

travel_year = input("What date would you like to travel to? YYYY-MM-DD ")
response = requests.get(url=f"{URL_ENDPOINT}{travel_year}")
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

song_names = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_list = [x.text for x in song_names]

artist_names = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
artist_list = [x.text for x in artist_names]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               show_dialog=True,
                                               scope="playlist-modify-private",
                                               cache_path="token.txt"))

user_id = sp.current_user()["id"]

uri_list = []

for x in range(100):
    result = sp.search(q=f"{song_list[x]} {artist_list[x]}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
    except IndexError:
        pass
    else:
        uri_list.append(uri)

playlist_id = sp.user_playlist_create(user=user_id, name=f"{travel_year} Billboard 100", public=False, collaborative=False, description=f"Billboard Top 100 of {travel_year}")["id"]

sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=uri_list)