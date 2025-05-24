let currentLyric = "";
let currentSong = "";
let hintCount = 0;
let usedLines = new Set();
let points = 0;

const lyricDisplay = document.getElementById("lyric");
const guessInput = document.getElementById("guessInput");
const resultDisplay = document.getElementById("result");
const pointsDisplay = document.getElementById("points");

function updatePoints(change) {
	points += change;
	pointsDisplay.textContent = points;
}

async function fetchLyric() {
	resultDisplay.textContent = "🎵 Loading...";
	try {
		const response = await fetch("/api/lyric");
		const data = await response.json();

		if (!data.lyric || usedLines.has(data.lyric)) {
			fetchLyric();
			return;
		}

		currentLyric = data.lyric;
		currentSong = data.song;
		hintCount = 0;
		lyricDisplay.textContent = currentLyric;
		resultDisplay.textContent = "";
	} catch (error) {
		resultDisplay.textContent = "⚠️ Failed to load lyric. Try again.";
	}
}

document.getElementById("guessBtn").addEventListener("click", () => {
	const guess = guessInput.value.trim().toLowerCase();
	if (!guess) return;

	if (guess === currentSong.toLowerCase()) {
		resultDisplay.textContent = "✅ Correct!";
		usedLines.add(currentLyric);
		updatePoints(1);
		guessInput.value = "";
		setTimeout(fetchLyric, 1500);
	} else {
		resultDisplay.textContent = "❌ Nope. Try again!";
	}
});

document.getElementById("skipBtn").addEventListener("click", () => {
	resultDisplay.textContent = `❕ It was: ${currentSong}`;
	usedLines.add(currentLyric);
	updatePoints(-1);
	guessInput.value = "";
	setTimeout(fetchLyric, 1500);
});

// Load the first lyric on page load
fetchLyric();
