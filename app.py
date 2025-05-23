from flask import Flask, jsonify, request, render_template
import os, random
from dotenv import load_dotenv
import lyricsgenius

load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")
genius = lyricsgenius.Genius(token, verbose=False)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

app = Flask(__name__)

@app.route('/api/lyric')
def api_lyric():
    return next_lyric()


albums = {
    "Blurryface": [
        "Heavydirtysoul", "Stressed Out", "Ride", "Fairly Local", "Tear in My Heart",
        "Lane Boy", "The Judge", "Doubt", "Polarize", "We Don't Believe What's on TV",
        "Message Man", "Hometown", "Not Today", "Goner"
    ],
    # Add more if you want
}

used_lines = set()
current_song = None
current_lyrics = []

def lyrics_clearer(lyrics):
    clean_lines = []
    for line in lyrics.strip().split("\n"):
        if line.startswith("[") and line.endswith("]"):
            continue
        if "Read More" in line or "… Read" in line or line.strip() == "":
            continue
        if line.lower().startswith("“") or line.lower().startswith("during") or "album" in line.lower():
            continue
        clean_lines.append(line.strip())
    return clean_lines

def fetch_song_lyrics(song_title):
    try:
        song = genius.search_song(song_title, artist="Twenty One Pilots")
        if not song:
            return []
        return lyrics_clearer(song.lyrics)
    except Exception as e:
        print(f"Error fetching {song_title}: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next-lyric')
def next_lyric():
    global current_song, current_lyrics, used_lines

    # If no current song or lyrics exhausted, pick a new song
    if not current_lyrics:
        available_songs = albums.get("Blurryface", [])
        if not available_songs:
            return jsonify({"status": "done", "message": "No songs available"})
        current_song = random.choice(available_songs)
        current_lyrics = [line for line in fetch_song_lyrics(current_song) if line not in used_lines]
        if not current_lyrics:
            return jsonify({"status": "done", "message": f"No lyrics found for {current_song}"})

    # Pop a lyric line to send
    lyric_line = current_lyrics.pop()
    used_lines.add(lyric_line)

    return jsonify({
        "status": "ok",
        "lyric": lyric_line,
        "song": current_song,
        "album": "Blurryface"
    })

@app.route('/reset')
def reset_game():
    global used_lines, current_lyrics, current_song
    used_lines = set()
    current_lyrics = []
    current_song = None
    return jsonify({"status": "ok", "message": "Game reset."})

if __name__ == '__main__':
    app.run(debug=True)
