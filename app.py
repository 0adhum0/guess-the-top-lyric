from flask import Flask, render_template, request, redirect, url_for
import os
import random
from dotenv import load_dotenv
import lyricsgenius

app = Flask(__name__)

load_dotenv()
token = os.getenv("GENIUS_API_TOKEN")
genius = lyricsgenius.Genius(token, verbose=False)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

# your `albums`, `lyrics_clearer`, `fetch_song_lyrics` functions go here

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_guess = request.form.get("guess", "").strip().lower()
        actual_song = request.form.get("song_title", "").lower()
        if user_guess == actual_song:
            return render_template("result.html", result="✅ Correct!", song_title=actual_song.title())
        else:
            return render_template("result.html", result="❌ Nope!", song_title=actual_song.title())

    # GET method
    song_title = random.choice(albums["Blurryface"])  # or pick randomly from all albums
    lyrics = fetch_song_lyrics(song_title)
    if not lyrics:
        return "Error: Could not fetch lyrics", 500

    lyric_line = random.choice(lyrics)

    return render_template("index.html", lyric_line=lyric_line, song_title=song_title)

if __name__ == "__main__":
    app.run(debug=True)
