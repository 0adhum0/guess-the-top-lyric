from flask import Flask, render_template, request, jsonify, session
import os
import random
from dotenv import load_dotenv
import lyricsgenius

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Load environment variables
load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")

# Initialize Genius API
genius = lyricsgenius.Genius(token, verbose=False)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

# Sample albums dictionary
albums = {
    "Blurryface": [
        "Heavydirtysoul", "Stressed Out", "Ride", "Fairly Local", "Tear in My Heart",
        "Lane Boy", "The Judge", "Doubt", "Polarize", "We Don't Believe What's on TV",
        "Message Man", "Hometown", "Not Today", "Goner"
    ]
    # Add other albums as needed
}

def fetch_song_lyrics(song_title):
    try:
        song = genius.search_song(song_title, artist="Twenty One Pilots")
        if not song:
            return None
        lyrics = song.lyrics
        # Clean lyrics
        lines = [line.strip() for line in lyrics.split('\n') if line and not line.startswith('[')]
        return lines
    except Exception as e:
        print(f"Error fetching {song_title}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/next')
def api_next():
    album = random.choice(list(albums.keys()))
    song = random.choice(albums[album])
    lyrics = fetch_song_lyrics(song)
    if not lyrics:
        return jsonify({'error': 'Could not fetch lyrics.'}), 500
    line = random.choice(lyrics)
    session['current_song'] = song
    session['current_album'] = album
    session['current_line'] = line
    return jsonify({'lyric': line})

@app.route('/api/guess', methods=['POST'])
def api_guess():
    data = request.get_json()
    guess = data.get('guess', '').strip().lower()
    actual = session.get('current_song', '').lower()
    if guess == actual:
        return jsonify({'correct': True, 'message': '✅ Correct!'})
    else:
        return jsonify({'correct': False, 'message': '❌ Nope!'})

@app.route('/api/hint')
def api_hint():
    album = session.get('current_album', '')
    return jsonify({'hint': f"The song is from the album '{album}'."})

if __name__ == '__main__':
    app.run(debug=True)
