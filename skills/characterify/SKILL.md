---
name: characterify
description: Install, run, and use Artify, a local video and image to colored character-art application.
---

# Characterify

Use this skill when the user asks to install Artify, start the local character-art app, convert a supplied image or video, or troubleshoot Artify.

## Supported user phrases

- “Install Characterify” or “Install Artify”
- “Start Characterify”
- “Characterify this video/image”
- “Convert this to character art”

## Installation workflow

1. Check whether the current directory is the Artify project. If it is not present, clone `https://github.com/KVSVikramaditya/Artify.git` into a user-chosen working directory. Do not overwrite an existing directory.
2. Create a Python virtual environment named `.venv` if one does not exist.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Start the app with the single command `python app.py`.
5. Tell the user that Artify opens at `http://127.0.0.1:5050` if their browser does not open automatically.

## Conversion workflow

1. Start the app.
2. Ask the user to use the + picker to select a local supported file, rather than handling copyrighted media downloads.
3. Explain the controls only if needed: Detail increases resolution and file size; Frames/sec only applies to videos.
4. The user presses **Artify**, waits for progress to reach 100%, previews the result, and uses **Save art**.

## Guardrails

- Everything runs locally. Do not upload media to external services.
- Do not delete original media or overwrite an existing output without the user's confirmation.
- Do not download media that the user may not have rights to use.
- Keep temporary files in `.artify/` and never commit them.
