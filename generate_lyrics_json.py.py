import os
import json
import random
from dotenv import load_dotenv
import lyricsgenius

# Load .env and Genius token
load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")
genius = lyricsgenius.Genius(token, verbose=False)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

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

lyrics_database = {}

for album, songs in albums.items():
    for title in songs:
        print(f"Fetching: {title}")
        try:
            song = genius.search_song(title, artist="Twenty One Pilots")
            if song:
                cleaned = lyrics_clearer(song.lyrics)
                lyrics_database[title] = {"album": album, "lyrics": cleaned}
        except Exception as e:
            print(f"Error fetching {title}: {e}")

with open("static/twenty_one_pilots_lyrics.json", "w") as f:
    json.dump(lyrics_database, f, indent=2)
print("✅ Lyrics saved to static/twenty_one_pilots_lyrics.json")
