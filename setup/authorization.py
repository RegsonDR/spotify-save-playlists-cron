import urllib.parse
from urllib.parse import parse_qs
from dotenv import load_dotenv, find_dotenv
import requests
import base64
import os

load_dotenv(find_dotenv())
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = "user-library-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"

def get_auth_url():
    payload = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }
    urlparams = urllib.parse.urlencode(payload)
    return ("%s?%s" % (OAUTH_AUTHORIZE_URL, urlparams))

def get_refresh_token(code):
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    encoded_client = base64.b64encode((CLIENT_ID + ":" + CLIENT_SECRET).encode('ascii'))
    headers = {"Authorization": "Basic %s" % encoded_client.decode('ascii')}
    response = requests.post(OAUTH_TOKEN_URL, data=payload, headers=headers)
    return response.json()['refresh_token']

def authorization():
    if CLIENT_ID is None or CLIENT_SECRET is None or REDIRECT_URI is None:
        print("Environment variables have not been loaded!")
        return

    print("Open this link in your browser: %s \n" % get_auth_url() )

    redirected_url = input("Enter URL you was redirected to (after accepting authorization): ")
    parsed_url = urllib.parse.urlparse(redirected_url)
    code = parse_qs(parsed_url.query)['code'][0]

    refresh_token = get_refresh_token(code)
    print("\n Your refresh token is: %s" % refresh_token)

authorization()
