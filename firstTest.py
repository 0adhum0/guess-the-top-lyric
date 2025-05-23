from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

token = os.environ.get("GENIUS_API_TOKEN")

if not token:
    print("Error: GENIUS_API_TOKEN not set")
    exit(1)

import lyricsgenius

genius = lyricsgenius.Genius(token)

song = genius.search_song("Stressed Out", "Twenty One Pilots")
if song:
    print(song.lyrics[:500])
else:
    print("Song not found.")
