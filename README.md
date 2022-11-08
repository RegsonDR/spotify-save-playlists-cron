# spotify-save-playlists-cron [![Save songs](https://github.com/RegsonDR/spotify-save-playlists-cron/actions/workflows/save.yaml/badge.svg)](https://github.com/RegsonDR/spotify-save-playlists-cron/actions/workflows/save.yaml)

This script automatically saves any of your playlists that have been generated & refreshed by Spotify, e.g "Discover Weekly". The songs from your temporary playlists are saved into a permanent playlist, using the Spotify API ([Authorization Code Flow](https://developer.spotify.com/documentation/general/guides/authorization/code-flow/)). The automation is powered by [Github Actions](https://docs.github.com/en/actions) and executes automatically everyday depending on your [playlist config](#4-playlist-configuration), playlists can be saved on a daily basis, or weekly based on certain specified days. Historically, this repository was created and used for automatically saving only the "Discover Weekly" playlist every week but it has now been extended to support multiple playlists on multiple days ([#3](https://github.com/RegsonDR/spotify-save-playlists-cron/pull/3)).

---

### (!) BREAKING CHANGE
This repository no longer uses `DISCOVER_WEEKLY_ID` or `SAVE_TO_ID` as environment variables, you will need to follow the set up from [step 4](#4-playlist-configuration) for it to continue working.

---

## Initial Set Up (approx: 10-15 minutes)
You should not need to make any commits back to the repo. [authorization.py](/setup/authorization.py) will help obtain the authorization data for setting up the environment variable in github secrets in order to allow `main.py` to execute properly. [playlist_config_builder.py](/setup/playlist_config_builder.py) will help you create a JSON string for your playlist configuration.

You need to fork this repo in order to have your own instance of github actions.

### (1) Create a Fork
Start off with simple fork by clicking on the "Fork" button. Once you've done that, you can use your favorite git client to clone your repo or use the command line:
```bash
# Clone your fork to your local machine
$ git clone https://github.com/<your-username>/spotify-save-playlists-cron.git
```

### (2) Librairies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all of the required librairies. You could use this with a [virtual environment](https://docs.python.org/3/library/venv.html) if required. 
```bash
$ pip install -r requirements.txt
```

### (3) Spotify API Credentials
1. Open the `.sample.env` file on your local machine. 
2. Sign into your [Spotify API Dashboard](https://developer.spotify.com/dashboard/applications) and create a new application. You can use any uri for the redirect uri, this is the base uri you will be redirected to after authorizing the app to access your account. If you see a "INVALID_CLIENT: Invalid redirect URI", then edit settings of your app from the spotify dashboard and add your uri as a redirect uri.
3. Fill out the env file with the same Client ID, Secret and Redirect URI details as found in step 3.2 and save this file as `.env`. **Do not post these details anywhere publically.**

Example:
```
CLIENT_ID=thisisanid
CLIENT_SECRET=thisisasecret
REDIRECT_URI=https://your.url/here
```
5. Execute [authorization.py](/setup/authorization.py) and open the URL generated in your browser. 
6. Authorize your app to access your Spotify account, this will then redirect you to your Redirect URI with a `?code=` parameter in the url.
7. Copy the whole url you were redirected to into the console and hit enter, this will then give you your refresh token. **Do not post this refresh token anywhere publically.**

Example:
 ```
$python authorization.py
Open this link in your browser: https://accounts.spotify.com/authorize?client_id=thisisanid&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2FRegsonDR&scope=user-library-read+playlist-modify-public+playlist-modify-private+playlist-read-private+playlist-read-collaborative

Enter URL you was redirected to (after accepting authorization):
> https://your.url/here?code=somecodehere

Your refresh token is: somerefreshtokenhere
```

### (4) Playlist Configuration
> To obtain Spotify playlist IDs, right click on a playlist > "Share" > "Copy link to playlist" (Example: `https://open.spotify.com/playlist/7EFfPnfospMihzWxcnitG1?si=16dcec3f35614e71`). The ID is of this playlist would be `7EFfPnfospMihzWxcnitG1`.

1. Open [playlist_config_builder.py](/setup/playlist_config_builder.py) on your local machine.
2. Populate the playlists_config dictionary variable with your configuration, one object for each playlist. 
  *  **day** (optional) - Index day of the week you want the playlist copied, e.g 0 for Monday, 4 for Friday. Leave this key out if you want daily execution.
  *  **source** (required) - The temporary spotify playlist ID you want to copy.
  *  **target** (required) - The permanent spotify playlist ID you want to copy to.
3. After you're done populating the dictionary, execute the [playlist_config_builder.py](/setup/playlist_config_builder.py) script and it will give you a stringified json of your configuration.

Example:
 ```
$python multi_playlist_builder.py
[{"day": 0, "source": "58x813F8Nv8YZJrPDplmV7", "target": "009M5VLWL1h66yW4gsl51S"},{"day": 4, "source": "17x813F8Nv8YZJrPDplm12", "target": "18cK5VLWL15P6yE4gSl110"},{"source": "124814587v88YZJrPDpl", "target": "05VLWL1hyW4l51S"}]
```

### (5) Github Actions
1. Go to the settings of your forked repo and click on "Secrets" > "Actions". 
2. You will need to create the following secrets:
  *  **CLIENT_ID** - Use the same Client ID from your `.env`.
  *  **CLIENT_SECRET** - Use the same Client Secret from your `.env`
  *  **REFRESH_TOKEN** - Use the refresh token generated in the [(3.7) Spotify API Credentials](#3-spotify-api-credentials) instructions above.
  *  **PLAYLISTS_CONFIG** - Use the stringified json created in [(4.3) Playlist Configuration](#4-playlist-configuration) instructions above.

![image](https://user-images.githubusercontent.com/32569720/200585494-7125568c-fe49-40a6-849b-13f092a01451.png)
---


## Manual Execution via Github Actions
1. Go to Actions in your forked repo.
2. Click on "Save songs"
3. Click on "Run workflow" which will bring up a drop down menu.
4. Click on "Run Workflow" again, this will initiate the script. Within the next few minutes, the script should execute and your songs should be in your new playlist in spotify.

Any execution errors can be found from within the actions tab of your forked repo.

![image](https://user-images.githubusercontent.com/32569720/113211386-4fa16580-926d-11eb-94c9-ddb513a122a7.png)

## Local Execution 
Alternatively, you can store the **REFRESH_TOKEN** & **PLAYLISTS_CONFIG** back into your `.env` file and execute `main.py` on your machine when required, maybe manually or using a task schedular.

```
$python main.py
```
---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
