from flask import Flask, render_template, request, redirect, url_for
import os
import random
from dotenv import load_dotenv
import lyricsgenius

app = Flask(__name__)

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

load_dotenv()
token = os.getenv("GENIUS_API_TOKEN")
genius = lyricsgenius.Genius(token, verbose=False)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

def lyrics_clearer(lyrics):
    """
    Cleans up the lyrics by removing section headers, empty lines,
    annotation remnants, and commentary blurbs.
    """
    clean_lines = []
    for line in lyrics.strip().split("\n"):
        # Remove section headers like [Chorus], [Verse 1]
        if line.startswith("[") and line.endswith("]"):
            continue
        # Remove annotation remnants or empty lines
        if "Read More" in line or "… Read" in line or line.strip() == "":
            continue
        # Remove Genius commentary blurbs
        if line.lower().startswith("“") or line.lower().startswith("during") or "album" in line.lower():
            continue
        clean_lines.append(line.strip())
    return clean_lines

def fetch_song_lyrics(song_title):
    """
    Fetches and cleans the lyrics for a given song title using the Genius API.
    Returns a list of lyric lines or None if not found.
    """
    try:
        song = genius.search_song(song_title, artist="Twenty One Pilots")
        if not song:
            return None
        return lyrics_clearer(song.lyrics)
    except Exception as e:
        print(f"Error fetching {song_title}: {e}")
        return None


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
