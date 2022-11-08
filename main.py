import requests, base64, json
from misc import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

REFRESH_TOKEN = get_env("REFRESH_TOKEN")
CLIENT_ID = get_env("CLIENT_ID")
CLIENT_SECRET = get_env("CLIENT_SECRET")
PLAYLISTS_CONFIG = get_env("PLAYLISTS_CONFIG")

OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"

DEBUG_WEEKDAYS = False # skips weekday recognition for easier testing

def refresh_access_token():
    payload = {
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
    }
    encoded_client = base64.b64encode((CLIENT_ID + ":" + CLIENT_SECRET).encode('ascii'))
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic %s" % encoded_client.decode('ascii')
    }
    response = requests.post(OAUTH_TOKEN_URL, data=payload, headers=headers)
    return response.json()

def get_playlist(access_token, playlist_id):
    url = "https://api.spotify.com/v1/playlists/%s" % playlist_id
    headers = {
       "Content-Type": "application/json",
       "Authorization": "Bearer %s" % access_token
    }
    response = requests.get(url, headers=headers)
    return response.json()

def add_to_playlist(access_token, tracklist, playlist_id):
    url = "https://api.spotify.com/v1/playlists/%s/tracks" % playlist_id
    payload = {
        "uris" : tracklist
    }
    headers = {
       "Content-Type": "application/json",
       "Authorization": "Bearer %s" % access_token
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

def copy_playlist(source, target):
    access_token = refresh_access_token()['access_token']
    playlist = get_playlist(access_token, source)

    try:
        tracks = playlist['tracks']
    except Exception as e: 
        raise ValueError('No tracks found, check the source')

    tracklist = []
    for item in tracks['items']:
        tracklist.append(item['track']['uri'])
    response = add_to_playlist(access_token, tracklist, target)

    if "snapshot_id" in response:
        print("Successfully added all", len(tracklist),"songs from", playlist['name'])
        return True
    else:
        print(response)
        return False

def process_multiple_playlists(config):
    current_week_day = get_weekday()
    handled_playlist_count = 0

    try:
        multi_playlist_info = json.loads(config)
    except Exception as e:
        print("Malformed JSON:", e)
        return handled_playlist_count

    for playlist_info in multi_playlist_info:
        should_handle = False
        try:
            required_week_day = playlist_info.get('day')
            source = playlist_info.get('source')
            target = playlist_info.get('target')

            if not source or not target:
                raise ValueError('Source or Target not defined')

            # If debugging or there isn't a day set
            if DEBUG_WEEKDAYS or required_week_day == None:
                should_handle = True

            # If there is a day set
            if  isinstance(required_week_day, int) and required_week_day == current_week_day:
                should_handle = True

            if should_handle and copy_playlist(source, target):
                handled_playlist_count += 1
                    
        except Exception as e: 
            print("Error:", e, "in", playlist_info)

    return handled_playlist_count

def main():
    print("Day index is", get_weekday(), "for", get_timestamp())
    if REFRESH_TOKEN == None or CLIENT_ID == None or CLIENT_SECRET == None:
        print("Auth token variables have not been loaded!")
        return

    if DEBUG_WEEKDAYS == True:
        print("Debug mode enabled")

    handled_playlist_count = process_multiple_playlists(PLAYLISTS_CONFIG)
    if handled_playlist_count == 0:
        print("No playlists handled. Have you set any playlist tokens in your .env for today?")
    else:
        print("Handled", handled_playlist_count, "playlist(s)")

main()