let currentAnswer = "";
let points = 0;

async function fetchLyric() {
	const response = await fetch("/api/lyric");
	const data = await response.json();

	const lyricBox = document.getElementById("lyric-box");
	const songReveal = document.getElementById("song-reveal");
	const feedback = document.getElementById("feedback");

	if (data.lyric) {
		currentAnswer = data.title.toLowerCase();
		lyricBox.textContent = data.lyric;
		songReveal.textContent = "";
		feedback.textContent = "";
		document.getElementById("guess-input").value = "";
	} else {
		lyricBox.textContent = "No more lyrics available!";
		currentAnswer = "";
	}
}

function updatePoints() {
	document.getElementById("points").textContent = points;
}

document.getElementById("submit-btn").addEventListener("click", () => {
	const guessInput = document.getElementById("guess-input");
	const feedback = document.getElementById("feedback");

	if (!currentAnswer) return;

	const userGuess = guessInput.value.trim().toLowerCase();
	if (userGuess === currentAnswer) {
		feedback.textContent = "✅ Correct!";
		points += 1;
		updatePoints();
		setTimeout(fetchLyric, 1000);
	} else {
		feedback.textContent = "❌ Nope! Try again.";
	}
});

document.getElementById("skip-btn").addEventListener("click", () => {
	const songReveal = document.getElementById("song-reveal");
	if (currentAnswer) {
		songReveal.textContent = `The answer was: ${currentAnswer}`;
	}
	setTimeout(fetchLyric, 2000);
});

window.onload = () => {
	fetchLyric();
};
