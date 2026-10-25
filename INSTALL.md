# Install Storytelling Motion

Run this guide when the user asks to install https://github.com/thomas3p/storytelling-motion. Respond in the user's language.

## 1. Host and checkout

- Detect the real host (Claude Code or Codex) and install for that host; install both only when asked.
- Clone into the user's tools folder (or download `archive/refs/heads/main.zip` when Git is missing):

  ```sh
  git clone https://github.com/thomas3p/storytelling-motion.git
  ```

  If a checkout already exists, update it with `git pull --ff-only` only when it has no local edits; never reset user work.

## 2. Install the skill and the workspace

Ask where the user keeps (or wants) the video workspace if it is not known, then run from the checkout:

```sh
python install.py --agent claude --workspace "<workspace>"      # Claude Code
python install.py --agent codex  --workspace "<workspace>"      # Codex
```

- Windows can use `py -3` or double-click `INSTALL-WINDOWS.cmd`; macOS/Linux may need `python3`.
- An identical existing install is a no-op. A different existing copy is skipped: show the user, and use `--replace` only with their agreement (the old copy is kept in `skill-backups/`).
- `--project "<folder>"` installs into one project instead of the user folder.
- The workspace step copies the pipeline into `<workspace>/tools` and the templates into `<workspace>/templates`, and creates `series/`, `projects/`, `logs/` and `assets/licences.md` without touching existing work.

## 3. Prerequisites (check, then tell the user what is missing)

| Need | Check | Install hint |
|---|---|---|
| Node.js 18+ | `node --version` | nodejs.org (HyperFrames runs through `npx hyperframes@<version>`) |
| Chrome | used by HyperFrames for capture | google.com/chrome |
| ffmpeg + ffprobe | `ffmpeg -version` | ffmpeg.org / `winget install Gyan.FFmpeg` |
| Python packages | `python -c "import soundfile, librosa, faster_whisper"` | `python -m pip install soundfile librosa faster-whisper` |
| Gemini API key | `GEMINI_API_KEY` is set (check only that it exists) | The user creates it in Google AI Studio and sets it in their own environment |

Never ask the user to paste an API key into the chat, never print or log its value, and mask any output that could contain it.

## 4. Smoke test

```sh
cd <workspace>
python tools/new_series.py --root . --slug demo --title "ทดสอบ" --episodes 1
python tools/new_episode.py --root . --series demo --ep 1 --title "ตอนทดลอง"
```

Write a one-phrase `voiceover/timings_final.json` (or generate a real voiceover per `references/voiceover.md`), then `python projects/<ep>/hf/build.py` and `npx hyperframes check --json` in that `hf/` folder. Report what worked; do not claim the TTS works until a real generation succeeded with the user's key.

## 5. Start

Tell the user to begin with `/storytelling-motion` (Claude Code) or `$storytelling-motion` (Codex) and a one-line story concept. Point them to `examples/characters/characters.html` for the example cast they can reuse.
