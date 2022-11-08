'''

This is a script to help you obtain your api refresh token which used when making api requests to spotify.

Fill in the .env file with your CLIENT_ID, CLIENT_SECRET & REDIRECT_URI and execute this script.
In the console it will output a link, click on it and authorize the oauth request, then copy the new
redirected url back into the console. It will strip out everything to get your refresh token, copy
this refresh token into your .env file for the REFRESH_TOKEN key.

'''

import urllib.parse, requests, base64, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from misc import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
CLIENT_ID = get_env("CLIENT_ID")
CLIENT_SECRET = get_env("CLIENT_SECRET")
REDIRECT_URI = get_env("REDIRECT_URI")

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
    if CLIENT_ID == None or CLIENT_SECRET == None or REDIRECT_URI == None:
        print("Environment variables have not been loaded!")
        return

    print("Open this link in your browser: %s \n" % get_auth_url() )

    redirected_url = input("Enter URL you was redirected to (after accepting authorization): ")
    parsed_url = urllib.parse.urlparse(redirected_url)
    code = urllib.parse.parse_qs(parsed_url.query)['code'][0]

    refresh_token = get_refresh_token(code)
    print("\n Your refresh token is: %s" % refresh_token)

authorization()
