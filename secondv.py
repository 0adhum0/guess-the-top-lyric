import os
import random
import logging
from dotenv import load_dotenv
import lyricsgenius

# Setup
logging.getLogger("lyricsgenius").setLevel(logging.CRITICAL)
load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")

if not token:
    print("GENIUS_API_TOKEN not set.")
    exit(1)

genius = lyricsgenius.Genius(token, verbose=False, remove_section_headers=True, skip_non_songs=True)
genius.timeout = 15

# Get full list of songs by artist
print("Fetching song list from Genius...")
artist = genius.search_artist("Twenty One Pilots", max_songs=20, sort="popularity")
songs = artist.songs
print(f"Loaded {len(songs)} songs.\n")

score = 0
rounds = 5

for _ in range(rounds):
    song = random.choice(songs)
    title = song.title
    lyrics_lines = song.lyrics.split("\n")
    lyrics_lines = [line for line in lyrics_lines if line.strip() and not line.startswith("[")]

    if not lyrics_lines:
        continue

    used_lines = []
    line = random.choice(lyrics_lines)
    used_lines.append(line)

    print("\n🎵 Guess the song from this lyric line:")
    print(f"\"{line}\"\n")

    # Input loop with hints
    while True:
        guess = input("Your guess (or type 'hint', 'skip', or 'quit'): ").strip().lower()

        if guess == "quit":
            print("Exiting game.")
            exit(0)
        elif guess == "skip":
            print(f"Skipped. It was: {title}\n")
            break
        elif guess == "hint":
            print(f"Hint: {len(title.split())} words, starts with \"{title[0]}\"")
            if len(used_lines) < len(lyrics_lines):
                new_line = random.choice([l for l in lyrics_lines if l not in used_lines])
                used_lines.append(new_line)
                print(f"Extra lyric line: \"{new_line}\"")
            else:
                print("No more hint lines available.")
        elif guess == title.lower():
            print("✅ Correct!\n")
            score += 1
            break
        else:
            print("❌ Incorrect. Try again or ask for a hint.")

print(f"\n🏁 Game Over. Final score: {score}/{rounds}")
