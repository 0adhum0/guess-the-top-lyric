from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

token = os.environ.get("GENIUS_API_TOKEN")

if not token:
    print("Error: GENIUS_API_TOKEN not set")
    exit(1)

import lyricsgenius

genius = lyricsgenius.Genius(token)

url = "https://genius.com/Twenty-one-pilots-stressed-out-lyrics"
if url:
    lyrics = genius.lyrics(song_url=url)
    print(lyrics.strip("More "))

else:
    print("Song not found.")
