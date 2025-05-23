import os
import random
import time
from dotenv import load_dotenv
import lyricsgenius

# Load .env
load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")
if not token:
    print("Error: GENIUS_API_TOKEN not set")
    exit(1)

# Genius setup
genius = lyricsgenius.Genius(token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], verbose=False)

# Albums and Songs
albums = {
    "Twenty One Pilots (2009)": [
        "Implicit Demand for Proof", "Fall Away", "The Pantaloon", "Addict with a Pen",
        "Friend, Please", "March to the Sea", "Johnny Boy", "Oh, Ms. Believer",
        "Air Catcher", "Trapdoor", "A Car, a Torch, a Death", "Taxi Cab",
        "Before You Start Your Day", "Isle of Flightless Birds"
    ],
    "Regional at Best (2011)": [
        "Guns for Hands", "Holding on to You", "Ode to Sleep", "Slowtown", "Car Radio",
        "Forest", "Glowing Eyes", "Kitchen Sink", "Anathema", "Lovely", "Ruby",
        "Trees", "Be Concerned", "Clear"
    ],
    "Vessel (2013)": [
        "Ode to Sleep", "Holding on to You", "Migraine", "House of Gold", "Car Radio",
        "Semi-Automatic", "Screen", "The Run and Go", "Fake You Out", "Guns for Hands",
        "Trees", "Truce"
    ],
    "Blurryface (2015)": [
        "Heavydirtysoul", "Stressed Out", "Ride", "Fairly Local", "Tear in My Heart",
        "Lane Boy", "The Judge", "Doubt", "Polarize", "We Don't Believe What's on TV",
        "Message Man", "Hometown", "Not Today", "Goner"
    ],
    "Trench (2018)": [
        "Jumpsuit", "Levitate", "Morph", "My Blood", "Chlorine", "Smithereens",
        "Neon Gravestones", "The Hype", "Nico and the Niners", "Cut My Lip",
        "Bandito", "Pet Cheetah", "Legend", "Leave the City"
    ],
    "Scaled and Icy (2021)": [
        "Good Day", "Choker", "Shy Away", "The Outside", "Saturday", "Never Take It",
        "Mulberry Street", "Formidable", "Bounce Man", "No Chances", "Redecorate"
    ],
    "Clancy (2024)": [
        "Overcompensate", "Next Semester", "Routines in the Night", "Midwest Indigo",
        "At the Risk of Feeling Dumb", "Oldies Station", "Backslide", "Vignette",
        "Lavish", "Navigating", "Snap Back", "Paladin Strait"
    ]
}

# Game setup
def get_user_selection():
    print("Choose a game mode:")
    print("1. All Songs")
    print("2. Choose Album")
    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        songs = [song for songs in albums.values() for song in songs]
    elif choice == "2":
        print("Available albums:")
        for i, album in enumerate(albums, 1):
            print(f"{i}. {album}")
        album_index = int(input("Enter album number: ")) - 1
        album_name = list(albums.keys())[album_index]
        songs = albums[album_name]
    else:
        print("Invalid choice")
        exit(1)

    return songs

def fetch_lyrics(song_title):
    try:
        song = genius.search_song(song_title, "Twenty One Pilots")
        if song and song.lyrics:
            lyrics = song.lyrics.split("Lyrics")[-1]  # remove intro
            return lyrics.strip().split("\n")
        return []
    except Exception as e:
        print(f"Error fetching lyrics for {song_title}: {e}")
        return []

def play_game(songs):
    seen_lines = set()
    while True:
        song = random.choice(songs)
        lines = fetch_lyrics(song)
        lines = [line.strip() for line in lines if line.strip() and line.strip() not in seen_lines]
        if not lines:
            continue
        random_line = random.choice(lines)
        seen_lines.add(random_line)

        print("\nGuess the song:")
        print(f"🧩: {random_line}")
        guess = input("Your guess (or 'q' to quit): ").strip()

        if guess.lower() == "q":
            print("Thanks for playing!")
            break
        elif guess.lower() == song.lower():
            print("✅ Correct!")
        else:
            print(f"❌ Nope! It was: {song}")

        hint = input("Need a hint? (y/n): ")
        if hint.lower() == "y":
            print(f"Hint: Album contains {len(songs)} songs.")

# Start
if __name__ == "__main__":
    selected_songs = get_user_selection()
    print("Fetching songs... please wait.\n")
    time.sleep(1)
    play_game(selected_songs)
