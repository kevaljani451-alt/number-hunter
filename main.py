import json
import os
import random
import secrets
import webbrowser
from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer


HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUMBER HUNTER - Number Guessing Game</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            background: #f2f5fb;
            color: #17213a;
            font-family: Arial, Helvetica, sans-serif;
        }

        .page {
            width: min(1050px, 92%);
            margin: 0 auto;
            padding: 28px 0 42px;
        }

        header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 34px;
            font-weight: bold;
            letter-spacing: 1.5px;
        }

        .logo {
            display: grid;
            width: 42px;
            height: 42px;
            place-items: center;
            border-radius: 13px;
            background: #635bdb;
            color: white;
            font-size: 23px;
        }

        .layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 42px;
            align-items: center;
        }

        .eyebrow {
            color: #635bdb;
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        h1 {
            margin: 12px 0;
            font-size: clamp(42px, 6vw, 66px);
            line-height: 1.02;
        }

        .intro {
            max-width: 430px;
            color: #65708a;
            font-size: 17px;
            line-height: 1.7;
        }

        .feature-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 24px;
        }

        .feature {
            padding: 9px 13px;
            border: 1px solid #e0e5f0;
            border-radius: 20px;
            background: white;
            color: #58627a;
            font-size: 13px;
        }

        .game-card {
            padding: 30px;
            border: 1px solid #e7eaf2;
            border-radius: 22px;
            background: white;
            box-shadow: 0 18px 55px rgba(37, 48, 82, 0.09);
        }

        .game-card h2 {
            margin: 0 0 8px;
            font-size: 25px;
        }

        .muted {
            color: #758099;
            line-height: 1.5;
        }

        .button {
            width: 100%;
            min-height: 48px;
            margin-top: 12px;
            padding: 12px 16px;
            border: 0;
            border-radius: 11px;
            background: #635bdb;
            color: white;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
        }

        .button:hover {
            background: #5149c5;
        }

        .button.secondary {
            border: 1px solid #dfe3ed;
            background: white;
            color: #313b55;
        }

        .button.secondary:hover {
            background: #f6f7fb;
        }

        .difficulty-list {
            display: grid;
            gap: 10px;
            margin-top: 20px;
        }

        .difficulty {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 15px;
            border: 1px solid #e3e7f0;
            border-radius: 12px;
            background: white;
            color: #222c45;
            text-align: left;
            cursor: pointer;
        }

        .difficulty:hover {
            border-color: #8179ec;
            background: #f8f7ff;
        }

        .difficulty strong,
        .difficulty span {
            display: block;
        }

        .difficulty small {
            display: block;
            margin-top: 4px;
            color: #758099;
        }

        .game-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }

        .level-pill {
            padding: 7px 11px;
            border-radius: 20px;
            background: #eeedff;
            color: #5149c5;
            font-size: 12px;
            font-weight: bold;
        }

        .attempts {
            margin: 22px 0 16px;
            padding: 15px;
            border-radius: 12px;
            background: #f5f6fa;
            color: #58627a;
            font-size: 14px;
        }

        .attempts strong {
            color: #222c45;
        }

        .guess-form {
            display: flex;
            gap: 9px;
        }

        .guess-form input {
            width: 100%;
            min-width: 0;
            padding: 13px;
            border: 1px solid #dfe3ed;
            border-radius: 10px;
            font-size: 16px;
        }

        .guess-form input:focus {
            border-color: #635bdb;
            outline: 2px solid #eeedff;
        }

        .guess-form .button {
            width: auto;
            min-width: 105px;
            margin: 0;
        }

        .message {
            min-height: 48px;
            margin: 16px 0 0;
            padding: 13px;
            border-radius: 10px;
            background: #f5f6fa;
            color: #46516a;
            line-height: 1.5;
        }

        .message.success {
            background: #eaf8f0;
            color: #187447;
        }

        .message.error {
            background: #fff0ed;
            color: #a63b2e;
        }

        .how-to {
            margin-top: 20px;
            padding: 15px;
            border-radius: 12px;
            background: #f5f6fa;
            color: #59647c;
            font-size: 14px;
            line-height: 1.6;
        }

        .how-to p {
            margin: 5px 0;
        }

        [hidden] {
            display: none !important;
        }

        footer {
            margin-top: 34px;
            color: #8891a5;
            font-size: 13px;
            text-align: center;
        }

        @media (max-width: 760px) {
            .page {
                padding-top: 20px;
            }

            .layout {
                grid-template-columns: 1fr;
                gap: 24px;
            }

            .game-card {
                padding: 23px;
            }
        }
    </style>
</head>
<body>
    <div class="page">
        <header>
            <div class="logo">?</div>
            <div>NUMBER HUNTER</div>
        </header>

        <main class="layout">
            <section>
                <div class="eyebrow">A little logic. A little luck.</div>
                <h1>Find the<br>hidden number.</h1>
                <p class="intro">
                    Pick a difficulty, make your guesses, and follow the clues.
                    How quickly can you find the number?
                </p>
                <div class="feature-list">
                    <span class="feature">Three difficulty levels</span>
                    <span class="feature">Earn points for a quick win</span>
                    <span class="feature">No extra installs</span>
                </div>
            </section>

            <section class="game-card">
                <div id="welcome-panel">
                    <h2>Ready to play?</h2>
                    <p class="muted">Your number-hunting challenge starts here.</p>
                    <button class="button" id="start-button">Start Game</button>
                    <button class="button secondary" id="how-button">How to Play</button>
                    <div class="how-to" id="how-to" hidden>
                        <p>1. Choose Easy, Medium, or Hard.</p>
                        <p>2. Guess a whole number in the shown range.</p>
                        <p>3. Use the high/low hints before attempts run out.</p>
                        <p>4. A correct guess earns base points plus 5 points per remaining attempt.</p>
                        <p>Numbers outside the range do not use an attempt.</p>
                    </div>
                    <div class="difficulty-list" id="difficulty-list" hidden>
                        <button class="difficulty" data-level="easy">
                            <span><strong>Easy</strong><small>1 to 20</small></span>
                            <span>7 attempts</span>
                        </button>
                        <button class="difficulty" data-level="medium">
                            <span><strong>Medium</strong><small>1 to 50</small></span>
                            <span>6 attempts</span>
                        </button>
                        <button class="difficulty" data-level="hard">
                            <span><strong>Hard</strong><small>1 to 100</small></span>
                            <span>5 attempts</span>
                        </button>
                    </div>
                </div>

                <div id="game-panel" hidden>
                    <div class="game-top">
                        <h2>Make your guess</h2>
                        <span class="level-pill" id="level-pill"></span>
                    </div>
                    <p class="muted" id="range-text"></p>
                    <div class="attempts">
                        Attempts remaining: <strong id="attempt-count"></strong>
                    </div>
                    <form class="guess-form" id="guess-form">
                        <input id="guess-input" type="number" step="1" required
                               placeholder="Enter a number" aria-label="Your guess">
                        <button class="button" id="guess-button" type="submit">Guess</button>
                    </form>
                    <p class="message" id="message" role="status">Good luck!</p>
                    <button class="button secondary" id="again-button" hidden>Play Again</button>
                    <button class="button secondary" id="menu-button">Change Difficulty</button>
                </div>
            </section>
        </main>

        <footer>NUMBER HUNTER - Guess smart and have fun.</footer>
    </div>

    <script>
        const welcomePanel = document.getElementById("welcome-panel");
        const gamePanel = document.getElementById("game-panel");
        const difficultyList = document.getElementById("difficulty-list");
        const howTo = document.getElementById("how-to");
        const guessForm = document.getElementById("guess-form");
        const guessInput = document.getElementById("guess-input");
        const guessButton = document.getElementById("guess-button");
        const messageBox = document.getElementById("message");
        const againButton = document.getElementById("again-button");
        let selectedLevel = "";

        async function sendRequest(path, values) {
            const response = await fetch(path, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(values)
            });
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message || "The request could not be completed.");
            }

            return result;
        }

        function showMessage(text, kind) {
            messageBox.textContent = text;
            messageBox.className = "message";
            if (kind) {
                messageBox.classList.add(kind);
            }
        }

        async function startGame(level) {
            try {
                const result = await sendRequest("/api/start", { level: level });
                selectedLevel = level;
                document.getElementById("level-pill").textContent = result.difficulty;
                document.getElementById("range-text").textContent =
                    "Guess a number from 1 to " + result.highest_number + ".";
                document.getElementById("attempt-count").textContent =
                    result.remaining_attempts;
                guessInput.min = 1;
                guessInput.max = result.highest_number;
                guessInput.value = "";
                guessInput.disabled = false;
                guessButton.disabled = false;
                againButton.hidden = true;
                showMessage("Your number is ready. Make your first guess!");
                welcomePanel.hidden = true;
                gamePanel.hidden = false;
                guessInput.focus();
            } catch (error) {
                showMessage(error.message, "error");
            }
        }

        document.getElementById("start-button").addEventListener("click", function () {
            howTo.hidden = true;
            difficultyList.hidden = false;
        });

        document.getElementById("how-button").addEventListener("click", function () {
            howTo.hidden = !howTo.hidden;
        });

        document.querySelectorAll(".difficulty").forEach(function (button) {
            button.addEventListener("click", function () {
                startGame(button.dataset.level);
            });
        });

        guessForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            if (!guessInput.reportValidity()) {
                return;
            }

            const guess = Number(guessInput.value);
            guessButton.disabled = true;

            try {
                const result = await sendRequest("/api/guess", { guess: guess });
                document.getElementById("attempt-count").textContent =
                    result.remaining_attempts;

                if (result.game_over) {
                    guessInput.disabled = true;
                    againButton.hidden = false;
                    if (result.won) {
                        showMessage(result.message + " Final score: " + result.score + " points.", "success");
                    } else {
                        showMessage(result.message + " The secret number was " +
                            result.secret_number + ". Final score: 0 points.", "error");
                    }
                } else {
                    showMessage(result.message);
                }

                guessInput.value = "";
            } catch (error) {
                showMessage(error.message, "error");
            } finally {
                if (!guessInput.disabled) {
                    guessButton.disabled = false;
                    guessInput.focus();
                }
            }
        });

        againButton.addEventListener("click", function () {
            startGame(selectedLevel);
        });

        document.getElementById("menu-button").addEventListener("click", function () {
            gamePanel.hidden = true;
            welcomePanel.hidden = false;
            difficultyList.hidden = false;
        });
    </script>
</body>
</html>
"""


class GameRequestHandler(BaseHTTPRequestHandler):
    """Serve the web page and handle its game requests."""

    games = {}

    def prepare_session(self):
        """Find this browser's game or create a new browser session."""
        cookies = SimpleCookie()
        try:
            cookies.load(self.headers.get("Cookie", ""))
        except CookieError:
            cookies = SimpleCookie()

        session_cookie = cookies.get("number_hunter_session")
        games = type(self).games

        if session_cookie and session_cookie.value in games:
            self.session_id = session_cookie.value
            self.new_session = False
        else:
            self.session_id = secrets.token_urlsafe(24)
            self.new_session = True
            games[self.session_id] = {"active": False}

    def send_json(self, status_code, result):
        """Send a JSON response to the browser."""
        response = json.dumps(result).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        if self.new_session:
            self.send_header(
                "Set-Cookie",
                "number_hunter_session=" + self.session_id + "; HttpOnly; SameSite=Lax; Path=/"
            )
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        """Send the game page when the browser visits the home address."""
        self.prepare_session()

        if self.path != "/" and self.path != "/index.html":
            self.send_error(404, "Page not found")
            return

        page = HTML_PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        if self.new_session:
            self.send_header(
                "Set-Cookie",
                "number_hunter_session=" + self.session_id + "; HttpOnly; SameSite=Lax; Path=/"
            )
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        """Start a game or check the player's guess."""
        self.prepare_session()
        content_length = int(self.headers.get("Content-Length", "0"))

        try:
            data = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except ValueError:
            self.send_json(400, {"message": "Please send valid game information."})
            return

        if not isinstance(data, dict):
            self.send_json(400, {"message": "Please send valid game information."})
            return

        if self.path == "/api/start":
            self.start_game(data)
        elif self.path == "/api/guess":
            self.check_guess(data)
        else:
            self.send_json(404, {"message": "Game action not found."})

    def start_game(self, data):
        """Choose a secret number and set the selected difficulty."""
        game = type(self).games[self.session_id]
        levels = {
            "easy": ("Easy", 20, 7, 10),
            "medium": ("Medium", 50, 6, 20),
            "hard": ("Hard", 100, 5, 30),
        }
        level = data.get("level")

        if not isinstance(level, str) or level not in levels:
            self.send_json(400, {"message": "Please choose a valid difficulty."})
            return

        (game["difficulty"], game["highest_number"],
         game["remaining_attempts"], game["base_points"]) = levels[level]
        game["secret_number"] = random.randint(1, game["highest_number"])
        game["active"] = True

        self.send_json(200, {
            "difficulty": game["difficulty"],
            "highest_number": game["highest_number"],
            "remaining_attempts": game["remaining_attempts"],
        })

    def check_guess(self, data):
        """Validate a guess, give a hint, and calculate the final score."""
        game = type(self).games[self.session_id]
        guess = data.get("guess")

        if not game["active"]:
            self.send_json(400, {"message": "Start a new game before guessing."})
            return

        if isinstance(guess, bool) or not isinstance(guess, int):
            self.send_json(400, {"message": "Enter a whole number."})
            return

        if guess < 1 or guess > game["highest_number"]:
            self.send_json(400, {
                "message": "Enter a number from 1 to " + str(game["highest_number"]) + "."
            })
            return

        game["remaining_attempts"] -= 1

        if guess == game["secret_number"]:
            score = game["base_points"] + (game["remaining_attempts"] * 5)
            game["active"] = False
            self.send_json(200, {
                "message": "Correct! You found the number. You win!",
                "remaining_attempts": game["remaining_attempts"],
                "game_over": True,
                "won": True,
                "score": score,
            })
        elif game["remaining_attempts"] == 0:
            game["active"] = False
            self.send_json(200, {
                "message": "No attempts left. You did not find the number.",
                "remaining_attempts": 0,
                "game_over": True,
                "won": False,
                "secret_number": game["secret_number"],
            })
        elif guess > game["secret_number"]:
            self.send_json(200, {
                "message": "Too High! Try a smaller number.",
                "remaining_attempts": game["remaining_attempts"],
                "game_over": False,
            })
        else:
            self.send_json(200, {
                "message": "Too Low! Try a bigger number.",
                "remaining_attempts": game["remaining_attempts"],
                "game_over": False,
            })


def main():
    """Start the local web server and open the game in a browser."""
    port = int(os.environ.get("PORT", "8000"))

    if "PORT" in os.environ:
        host = "0.0.0.0"
        print("NUMBER HUNTER server is starting.")
    else:
        host = "127.0.0.1"
        address = "http://127.0.0.1:" + str(port)
        print("NUMBER HUNTER is running at " + address)
        print("Keep this window open while you play. Press Ctrl+C to stop the server.")
        webbrowser.open(address)

    server = HTTPServer((host, port), GameRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
