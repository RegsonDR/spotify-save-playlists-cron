from dotenv import load_dotenv, find_dotenv
import requests
import base64
import json

from misc import *

load_dotenv(find_dotenv())

REFRESH_TOKEN = get_env("REFRESH_TOKEN")
CLIENT_ID = get_env("CLIENT_ID")
CLIENT_SECRET = get_env("CLIENT_SECRET")
DISCOVER_WEEKLY_ID = get_env("DISCOVER_WEEKLY_ID")
SAVE_TO_ID = get_env("SAVE_TO_ID")
MULTIPLE_PLAYLIST_CONFIG = get_env("MULTIPLE_PLAYLIST_CONFIG")

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


def get_playlist(access_token, playlistID):
    url = "https://api.spotify.com/v1/playlists/%s" % playlistID
    headers = {
       "Content-Type": "application/json",
       "Authorization": "Bearer %s" % access_token
    }
    response = requests.get(url, headers=headers)
    return response.json()

def add_to_playlist(access_token, tracklist, playlistID):
    url = "https://api.spotify.com/v1/playlists/%s/tracks" % playlistID
    payload = {
        "uris" : tracklist
    }
    headers = {
       "Content-Type": "application/json",
       "Authorization": "Bearer %s" % access_token
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

def handle_playlist(source, target):
    access_token = refresh_access_token()['access_token']
    tracks =  get_playlist(access_token, source)['tracks']['items']
    tracklist = []
    for item in tracks:
        tracklist.append(item['track']['uri'])
    response = add_to_playlist(access_token, tracklist, target)

    if "snapshot_id" in response:
        print("Successfully added all songs from", source)
        return True
    else:
        print(response)
        return False

def process_discover_weekly_playlist():
    if DEBUG_WEEKDAYS or get_weekday() == 1: #only run on Monday
        if handle_playlist(DISCOVER_WEEKLY_ID, SAVE_TO_ID):
            return 1
    return 0

def process_multiple_playlists(config):

    handled_playlist_count = 0

    try:
        multi_playlist_info = json.loads(config)
    except Exception as e:
        print("Malformed JSON:", e)
        return handled_playlist_count

    for playlist_info in multi_playlist_info:

        try:
            day = playlist_info.get('day')
            source = playlist_info.get('source')
            target = playlist_info.get('target')

            if not DEBUG_WEEKDAYS and day and isinstance(day, int):

                if(day != get_weekday()): 
                    #if a weekday is set, don't add them on other weekdays
                    break

            if(source and target):
                if handle_playlist(source, target):
                    handled_playlist_count += 1
            else:
                raise ValueError('Source or Target not defined')

        except Exception as e: 
            print("Error:", e, "in", playlist_info)

    return handled_playlist_count


def main():

    handled_playlist_count = 0

    if REFRESH_TOKEN is None or CLIENT_ID is None or CLIENT_SECRET is None:
        print("Auth token variables have not been loaded!")
        return

    # default functionaliy with a single "Discover Weekly" playlist
    if DISCOVER_WEEKLY_ID and SAVE_TO_ID:
        handled_playlist_count += process_discover_weekly_playlist()

    # multiple playlists option, see `multi_playlist_builder.py`
    if MULTIPLE_PLAYLIST_CONFIG:
        handled_playlist_count += process_multiple_playlists(MULTIPLE_PLAYLIST_CONFIG)


    if handled_playlist_count == 0:
        print("No playlists handled. Have you set any playlist tokens in your .env?")
    else:
        print("Handled", handled_playlist_count, "playlist(s)")


main()