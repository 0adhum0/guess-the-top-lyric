import os
import random
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import lyricsgenius

load_dotenv()
app = Flask(__name__)

# Genius API
GENIUS_TOKEN = os.getenv("GENIUS_API_TOKEN")
if not GENIUS_TOKEN:
    raise EnvironmentError("GENIUS_API_TOKEN not set in .env file")

genius = lyricsgenius.Genius(GENIUS_TOKEN, verbose=False)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

albums = {
    "Twenty One Pilots": [
        "Implicit Demand for Proof", "Fall Away", "The Pantaloon", "Addict with a Pen",
        "Friend, Please", "March to the Sea", "Johnny Boy", "Oh Ms Believer",
        "Air Catcher", "Trapdoor", "A Car, a Torch, a Death", "Taxi Cab",
        "Before You Start Your Day", "Isle of Flightless Birds"
    ],
    "Regional at Best": [
        "Guns for Hands", "Holding on to You", "Ode to Sleep", "Slowtown",
        "Car Radio", "Forest", "Glowing Eyes", "Kitchen Sink", "Anathema",
        "Lovely", "Ruby", "Trees", "Be Concerned", "Clear", "Screen", "House of Gold"
    ],
    "Vessel": [
        "Ode to Sleep", "Holding on to You", "Migraine", "House of Gold", "Car Radio",
        "Semi-Automatic", "Screen", "The Run and Go", "Fake You Out", "Guns for Hands",
        "Trees", "Truce"
    ],
    "Blurryface": [
        "Heavydirtysoul", "Stressed Out", "Ride", "Fairly Local", "Tear in My Heart",
        "Lane Boy", "The Judge", "Doubt", "Polarize", "We Don't Believe What's on TV",
        "Message Man", "Hometown", "Not Today", "Goner"
    ],
    "Trench": [
        "Jumpsuit", "Levitate", "Morph", "My Blood", "Chlorine", "Smithereens",
        "Neon Gravestones", "The Hype", "Nico and the Niners", "Cut My Lip",
        "Bandito", "Pet Cheetah", "Legend", "Leave the City"
    ],
    "Scaled and Icy": [
        "Good Day", "Choker", "Shy Away", "The Outside", "Saturday", "Never Take It",
        "Mulberry Street", "Formidable", "Bounce Man", "No Chances", "Redecorate"
    ],
    "Clancy": [
        "Overcompensate", "Next Semester", "Midwest Indigo", "Routines in the Night",
        "Vignette", "The Craving (Jenna's Version)", "Lavish", "Navigating",
        "Snap Back", "Oldies Station", "At the Risk of Feeling Dumb", "Paladin Strait"
    ]
}

used_lyrics = set()
current_song = None
current_lyrics = []
current_line = ""
points = 0


def lyrics_clearer(lyrics):
    lines = []
    for line in lyrics.strip().split("\n"):
        if line.startswith("[") and line.endswith("]"):
            continue
        if "Read More" in line or "… Read" in line or line.strip() == "":
            continue
        lines.append(line.strip())
    return lines


def fetch_lyrics(song_title):
    try:
        song = genius.search_song(song_title, artist="Twenty One Pilots")
        if song:
            return lyrics_clearer(song.lyrics)
    except Exception as e:
        print("Error fetching lyrics:", e)
    return []


def pick_new_lyric():
    global current_song, current_lyrics, current_line
    for _ in range(10):
        album = random.choice(list(albums.keys()))
        song_title = random.choice(albums[album])
        lyrics = fetch_lyrics(song_title)
        lyrics = [line for line in lyrics if line not in used_lyrics]
        if lyrics:
            current_song = song_title
            current_lyrics = lyrics
            current_line = random.choice(lyrics)
            return True
    return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/lyric")
def get_lyric():
    if pick_new_lyric():
        return jsonify({"lyric": current_line})
    return jsonify({"lyric": None})


@app.route("/api/guess", methods=["POST"])
def make_guess():
    global points
    data = request.json
    guess = data.get("guess", "").strip().lower()
    if guess == current_song.lower():
        used_lyrics.update(current_lyrics)
        points += 1
        return jsonify({"correct": True, "song": current_song, "points": points})
    return jsonify({"correct": False})


@app.route("/api/reveal")
def reveal():
    return jsonify({"song": current_song})


@app.route("/api/points")
def get_points():
    return jsonify({"points": points})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
