# Artify contributor guide

## Purpose

Artify converts local videos and images into colored character art. It runs entirely on the user's computer; do not add cloud uploads, tracking, or hidden network calls. The reusable user-facing workflow is named **Characterify**; see `skills/characterify/SKILL.md`.

## Agent entry points

When a user says “Install Characterify,” “Start Characterify,” or “Characterify this,” load `skills/characterify/SKILL.md` and follow it. Explain actions before performing them, keep source files intact, and never silently publish results.

## Quick start

```bash
git clone https://github.com/KVSVikramaditya/artify.git
cd artify
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

The app opens at `http://127.0.0.1:5050`. Use the file picker, choose media, press **Artify**, then use **Save art** when the preview is ready.

## Architecture

- `app.py`: local browser launcher.
- `src/web.py`: Flask routes, upload validation, jobs, and progress status.
- `src/media.py`: shared image/video rendering service.
- `src/renderer.py`: raster-to-character drawing.
- `src/frame_processor.py`: color adjustment and downsampling.
- `src/video_reader.py` and `src/gif_exporter.py`: video input and animated GIF output.
- `templates/` and `static/`: browser interface.

## Contributor rules

- Keep rendering offline and deterministic.
- Preserve the CLI: `python main.py INPUT --output OUTPUT`.
- Put temporary uploads and results only in `.artify/`; never commit them.
- Add tests for pure rendering or parsing behavior in `tests/`.
- Prefer GIF for animated video output and PNG for image output.
- Do not download copyrighted source clips on a user's behalf. Users must supply files they have the right to use.
