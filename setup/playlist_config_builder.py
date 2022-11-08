'''

This is a small helper to build your playlist array.

The array contains dictionaries with a

source: The id of the playlist to copy
target: The id of the playlist to copy the songs to
day:    (optional) If you only want to add to a playlist on a particular weekday.
        This makes sense for most weekly playlists. Monday is 0, Friday is 4 etc.

Fill in the data in the playlists_config and run the file to gather the processed JSON.

After generating the JSON, copy it to the PLAYLISTS_CONFIG= section. You don't need to put extra quotes,
but you need to include the square brackets so for a playlist saved every Wednesday it looks like:

PLAYLISTS_CONFIG=[{"day": 2, .....]

'''

import json

playlists_config = [

    # Discover Weekly example
    {
    "day": 0, # will only run on Mondays
    "source": "",
    "target": ""
    },

    # Release Radar example
    {
    "day": 4, # will only run on Fridays
    "source": "",
    "target": ""
    }

]

playlists_json = json.dumps(playlists_config)

# Copy this JSON String from your console into your .env file for the PLAYLISTS_CONFIG key.
print(f'\n{playlists_json}\n')