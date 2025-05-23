import os
import random
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import lyricsgenius

# Load environment variables
load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")

if not token:
    raise RuntimeError("GENIUS_API_TOKEN not set in environment")

genius = lyricsgenius.Genius(token, verbose=False)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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

used_lyrics_lines = set()
current_song_data = {}  # To keep track of current lyric, song, album

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
            return None
        return lyrics_clearer(song.lyrics)
    except Exception as e:
        print(f"Error fetching {song_title}: {e}")
        return None

def choose_song():
    # Choose from all albums for simplicity
    song_list = []
    for songs in albums.values():
        song_list.extend(songs)
    if not song_list:
        return None
    return random.choice(song_list)

def prepare_next_lyric():
    global used_lyrics_lines, current_song_data
    while True:
        song_title = choose_song()
        if not song_title:
            return None
        lyrics = fetch_song_lyrics(song_title)
        if not lyrics:
            continue
        # Filter out used lines
        new_lyrics = [line for line in lyrics if line not in used_lyrics_lines]
        if not new_lyrics:
            continue

        lyric_line = random.choice(new_lyrics)
        # Find album for song
        song_album = None
        for album, songs in albums.items():
            if song_title in songs:
                song_album = album
                break
        current_song_data = {
            "lyric": lyric_line,
            "song": song_title,
            "album": song_album,
            "lyrics_all": lyrics
        }
        return current_song_data

@app.route("/api/lyric")
def api_lyric():
    data = prepare_next_lyric()
    if not data:
        return jsonify({"error": "No songs/lyrics available"}), 404
    return jsonify({
        "lyric": data["lyric"],
        "album": data["album"]
    })

@app.route("/api/guess", methods=["POST"])
def api_guess():
    global used_lyrics_lines, current_song_data
    guess = request.json.get("guess", "").strip().lower()
    if not current_song_data:
        return jsonify({"error": "No lyric loaded"}), 400
    correct_song = current_song_data["song"].lower()
    if guess == correct_song:
        # Mark all lyrics lines as used for this song
        for line in current_song_data["lyrics_all"]:
            used_lyrics_lines.add(line)
        answer = current_song_data["song"]
        current_song_data = {}
        return jsonify({"correct": True, "message": f"Correct! The song was '{answer}'."})
    else:
        # User gave wrong guess, show song anyway after skipping
        return jsonify({"correct": False, "message": "Wrong guess! Try again or skip."})

@app.route("/api/skip", methods=["POST"])
def api_skip():
    global used_lyrics_lines, current_song_data
    if not current_song_data:
        return jsonify({"error": "No lyric loaded"}), 400
    # Mark all lyrics lines as used for this song (skip)
    for line in current_song_data["lyrics_all"]:
        used_lyrics_lines.add(line)
    answer = current_song_data["song"]
    current_song_data = {}
    return jsonify({"message": f"Skipped! The song was '{answer}'."})

if __name__ == "__main__":
    app.run(debug=True)
