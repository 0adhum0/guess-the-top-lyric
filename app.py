from flask import Flask, render_template, jsonify, request, session
import random, json

app = Flask(__name__)
app.secret_key = "supersecretkey"

with open("albums.json") as f:
    albums = json.load(f)

all_songs = [(album, song) for album, songs in albums.items() for song in songs]

@app.route("/")
def index():
    session['points'] = 0
    return render_template("index.html")

@app.route("/new-song")
def new_song():
    album, song = random.choice(all_songs)
    session['answer'] = song
    return jsonify({"hint": f"The song is from '{album}'", "points": session['points']})

@app.route("/guess", methods=["POST"])
def guess():
    guess = request.json.get("guess")
    correct = guess.strip().lower() == session.get("answer", "").lower()
    if correct:
        session['points'] += 10
    return jsonify({"correct": correct, "points": session['points']})
