from dotenv import load_dotenv
import os
import lyricsgenius

load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")

if not token:
    print("Error: GENIUS_API_TOKEN not set")
    exit(1)


def lyrics_clearer(lyrics):
    # Remove the "More" section from the lyrics
    stepOne = lyrics.split("More\xa0")
    del stepOne[0]
    clean_lyrics = " ".join(stepOne)
    return clean_lyrics

genius = lyricsgenius.Genius(token)

url = input("Enter Song URL: ")
if url:
    lyrics = genius.lyrics(song_url=url)
    clean_lyrics = lyrics_clearer(lyrics)
    print(clean_lyrics)
else:
    print("Song not found.")


