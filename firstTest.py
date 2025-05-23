from dotenv import load_dotenv
import os
import lyricsgenius

load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")

if not token:
    print("Error: GENIUS_API_TOKEN not set")
    exit(1)

genius = lyricsgenius.Genius(token)

url = "https://genius.com/Twenty-one-pilots-stressed-out-lyrics"
if url:
    lyrics = genius.lyrics(song_url=url)
    clean_lyrics = lyrics.split("More ")[0].strip()  # split at 'More ' and keep the first part
    print(clean_lyrics)
else:
    print("Song not found.")
