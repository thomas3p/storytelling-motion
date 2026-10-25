# Third-party notices

This repository contains only original code, documentation and example characters (MIT). It does not bundle any of the following; they are fetched or used at run time under their own terms.

| Component | Use | Terms |
|---|---|---|
| [HyperFrames](https://hyperframes.heygen.com) (`npx hyperframes`) | renders HTML compositions to video | see its npm package licence |
| [GSAP](https://gsap.com) (loaded from jsDelivr in `index.html`) | timeline animation | GSAP standard licence (free for this use) |
| [Prompt](https://fonts.google.com/specimen/Prompt), [Mitr](https://fonts.google.com/specimen/Mitr), [Kanit](https://fonts.google.com/specimen/Kanit) | Thai typefaces, downloaded by `scripts/get_fonts.py` | SIL Open Font License 1.1 |
| [freesound.org](https://freesound.org) sounds | sound effects and music, searched with `scripts/fs_search.py` (CC0 only) | CC0 1.0 — record each file in `assets/licences.md` |
| Gemini TTS (Google AI Studio API) | voiceover, with the user's own API key | Google's API terms; check commercial-use terms before monetising |
| faster-whisper, librosa, soundfile | transcription, pitch and audio I/O | their own open-source licences |

The "flood" look of `scripts/flatkit.js` was designed for this workflow (reference project `survival-5styles`); the example cast in `templates/series-flood/` is fictional.
