pipimport spotipy
import config
from spotipy.oauth2 import SpotifyOAuth
import interface as ui
import webbrowser

# declaring scope
scope = "user-read-recently-played playlist-modify-public playlist-modify-private"
uri = "http://localhost:8080/"
ui_green = "#1ED760"
ui_black = "#191414"
ui_white = "#FFFFFF"


def close_window(window):
    window.destroy()


ui.main_page()
# authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=config.CLIENT_ID,
                                               client_secret=config.CLIENT_SECRET, redirect_uri=uri))
history = sp.current_user_recently_played(20)    # API request to get listening history


track_checkbox = {}
track_dict = {}
tracks = []
for idx, items in enumerate(history['items']):          # storing tracks with artists for displaying & IDs for accessing
    track = items['track']                              # to access tracks as history is a nested dict
    track_dict.__setitem__(track['name'] + ' - ' + track['artists'][0]['name'], track['id'])
    track_checkbox.__setitem__(track['name'] + ' - ' + track['artists'][0]['name'], 0)  # make track list for ui purpose


ui.show_checkboxes(track_checkbox)
seed_tracks_names = ui.checked_boxes()                  # track names and artists returned
seed_track_ids = [track_dict[track] for track in seed_tracks_names]
limit = 50

# visualising history
"""for idx, track in enumerate(tracks):
    print(str(idx+1) + '.', track)
"""
# prompt user to select songs as seeds
# generating recommendations
recommend = sp.recommendations(seed_tracks=seed_track_ids, limit=limit)

# displaying recommendations
# print("\nHere are the recommended tracks which will be included in your new playlist:")

recommended_tracks = {}
for idx, track in enumerate(recommend['tracks']):
    print(f"{idx+1}. {track['name']} - {track['artists'][0]['name']}")
    recommended_tracks.__setitem__(track['name'] + ' - ' + track['artists'][0]['name'], track['id'])

ui.show_recommendations(recommended_tracks)

user = sp.me()
playlist_name = "Your Spot-on-ify Playlist"
recommendations_ids = [recommended_tracks[name] for name in list(recommended_tracks.keys())]
playlist = sp.user_playlist_create(user['id'], name=playlist_name, description="Recommended by Spot-on-ify")
sp.playlist_add_items(playlist['id'], recommendations_ids)

spotify_website = "https://open.spotify.com/playlist/" + playlist['id']
webbrowser.open(spotify_website)

sp.__del__()
