import os
import random
from dotenv import load_dotenv
import lyricsgenius

load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")

if not token:
    print("Error: GENIUS_API_TOKEN not set")
    exit(1)

genius = lyricsgenius.Genius(token, verbose=False)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

def lyrics_clearer(lyrics):
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

albums = {
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
    ]
}

def fetch_song_lyrics(song_title):
    try:
        song = genius.search_song(song_title, artist="Twenty One Pilots")
        if not song:
            return None
        return lyrics_clearer(song.lyrics)
    except Exception as e:
        print(f"Error fetching {song_title}: {e}")
        return None

def choose_song(album=None):
    if album:
        song_list = albums.get(album, [])
    else:
        # all songs from all albums
        song_list = []
        for songs in albums.values():
            song_list.extend(songs)
    if not song_list:
        print("No songs found.")
        return None
    return random.choice(song_list)

def main():
    print("Choose a game mode:")
    print("1. All Songs")
    print("2. Choose Album")
    choice = input("Enter choice (1 or 2): ").strip()
    selected_album = None

    if choice == "2":
        print("\nAvailable albums:")
        for idx, album_name in enumerate(albums.keys(), 1):
            print(f"{idx}. {album_name}")
        album_choice = input("Enter album number: ").strip()
        try:
            album_index = int(album_choice) - 1
            selected_album = list(albums.keys())[album_index]
        except (ValueError, IndexError):
            print("Invalid album choice, defaulting to all songs.")
            selected_album = None

    print("\nFetching songs... please wait.\n")

    used_lyrics_lines = set()

    while True:
        song_title = choose_song(selected_album)
        if not song_title:
            print("Could not get a song, exiting.")
            break

        lyrics = fetch_song_lyrics(song_title)
        if not lyrics:
            print(f"Could not fetch lyrics for {song_title}, trying another song...")
            continue

        # Remove repeated lyric lines already used
        new_lyrics = [line for line in lyrics if line not in used_lyrics_lines]
        if not new_lyrics:
            # All lyrics lines used, pick another song
            continue

        # Pick a random lyric line as the puzzle
        lyric_line = random.choice(new_lyrics)

        print("Guess the song:")
        print(f"🧩: {lyric_line}")

        guess = input("Your guess (or 'q' to quit): ").strip().lower()
        if guess == "q":
            print("Thanks for playing!")
            break

        if guess == song_title.lower():
            print("✅ Correct!")
            # Mark these lines as used
            for line in lyrics:
                used_lyrics_lines.add(line)
        else:
            print(f"❌ Nope! It was: {song_title}")

        hint_req = input("Need a hint? (y/n): ").strip().lower()
        if hint_req == "y":
            if selected_album:
                print(f"Hint: The song is from the album '{selected_album}'.")
            else:
                # Give the album as a hint
                song_album = None
                for album, songs in albums.items():
                    if song_title in songs:
                        song_album = album
                        break
                print(f"Hint: The song is from the album '{song_album}'.")

if __name__ == "__main__":
    main()
