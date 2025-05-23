import os
import random
from dotenv import load_dotenv
import lyricsgenius

load_dotenv()
token = os.environ.get("GENIUS_API_TOKEN")

if not token:
    print("Error: GENIUS_API_TOKEN not set.")
    exit(1)

genius = lyricsgenius.Genius(token)

# List of song titles (expand as needed)
songs = [
    "Stressed Out",
    "Ride",
    "Heathens",
    "Tear in My Heart",
    "Car Radio",
    "Lane Boy",
]

artist = "Twenty One Pilots"

# Score
score = 0
rounds = 3  # you can make it infinite with while True

for _ in range(rounds):
    # Pick a random song
    title = random.choice(songs)
    song = genius.search_song(title, artist)

    if not song:
        print(f"Couldn't find lyrics for {title}")
        continue

    # Clean and split lyrics
    lyrics = song.lyrics
    lyrics_lines = lyrics.split("\n")
    # Filter out empty and section headers like [Verse]
    lyrics_lines = [line for line in lyrics_lines if line and not line.startswith("[")]

    # Pick a random line to show
    random_line = random.choice(lyrics_lines)
    print("\n🎵 Guess the song from this line:")
    print(f"\"{random_line}\"\n")

    guess = input("Your guess: ").strip().lower()
    if guess == title.lower():
        print("✅ Correct!\n")
        score += 1
    else:
        print(f"❌ Nope! It was: {title}\n")

print(f"Game over. Your score: {score}/{rounds}")
