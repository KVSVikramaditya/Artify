# Artify — Video to Character Art

Turn videos and images into vivid character art made from letters, numbers, dots, and symbols. Artify is a small, local-first creative tool: no account, cloud upload, or tracking required.

## Run the browser app

Python 3.10+ is recommended.

```bash
git clone https://github.com/KVSVikramaditya/artify.git
cd artify
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Your browser opens to `http://127.0.0.1:5050`. Pick a video or image, tune the detail level, click **Artify**, watch the live render progress, preview the result, then choose **Save art**. The browser's normal download setting determines the final save location.

### Supported inputs

- Video: MP4, MOV, MKV, AVI, WEBM → animated GIF
- Image: PNG, JPG, JPEG, WEBP, BMP → PNG

## Command line

The renderer also works without the UI:

```bash
python main.py clip.mp4 --output output/demo.gif --width 140 --fps 10
python main.py photo.jpg --output output/photo-art.png --width 160
```

Use `python main.py --help` for options such as `--start`, `--duration`, `--contrast`, `--saturation`, `--digits`, and `--font-size`.

## Project layout

```text
app.py              # browser app launcher
main.py             # command-line launcher
src/                # rendering engine and local web service
templates/          # HTML UI
static/             # CSS and browser-side progress UI
tests/              # automated checks
AGENTS.md           # contributor and agent guide
skills/characterify # reusable install-and-convert agent skill
```

## Agent-assisted setup: Characterify

Artify includes a portable agent workflow called **Characterify**. In a compatible coding agent, open the project and say:

```text
Install Characterify
Start Characterify
Characterify this video
```

The agent instructions live in `AGENTS.md` and `skills/characterify/SKILL.md`. A standalone collection with adapters for Codex, Cursor, and VS Code/Copilot is available in the `vikramaditya-agents/` package. Copy the adapter for your tool into the project that will use it, then start a chat with one of the phrases above. Agent instructions guide a compatible tool; they do not execute by themselves.

## Use cases

- Build animated GitHub profile banners and README demos.
- Create stylized social posts, album art, posters, and terminal-inspired visuals.
- Explore image processing through a readable, character-based representation.

Only process media you have the right to use. Temporary files live in `.artify/` and are ignored by Git.
