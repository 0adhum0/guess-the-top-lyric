let hintEl = document.getElementById("hint");
let pointsEl = document.getElementById("points");
let resultEl = document.getElementById("result");

function newSong() {
	fetch("/new-song")
		.then((res) => res.json())
		.then((data) => {
			hintEl.textContent = data.hint;
			pointsEl.textContent = data.points;
			resultEl.textContent = "";
		});
}

function submitGuess() {
	let guess = document.getElementById("guessInput").value;
	fetch("/guess", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ guess }),
	})
		.then((res) => res.json())
		.then((data) => {
			resultEl.textContent = data.correct ? "Correct!" : "Wrong!";
			pointsEl.textContent = data.points;
		});
}

window.onload = newSong;
