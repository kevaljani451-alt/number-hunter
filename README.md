# NUMBER HUNTER

A browser-based number guessing game served by a small Python web server.
The game uses only Python's standard library.

## Run locally

1. Install Python 3.
2. Open a terminal in this folder.
3. Run `python main.py`.
4. The game opens at <http://127.0.0.1:8000>.
5. Keep the terminal open while playing. Press Ctrl+C to stop the server.

## Deploy on Render

This repository includes a Render Blueprint in `render.yaml`.
Create a new Blueprint in Render and select this public GitHub repository.
Render will build and start the Python web server and provide a public URL.

Each browser gets its own game session.
