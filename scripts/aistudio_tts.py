"""Generate a voiceover with the Gemini TTS API (Google AI Studio) using a fixed seed and a low temperature,
so every episode of a series comes out of the same settings. The web UI can lower temperature but has no seed.

usage:
  python tools/aistudio_tts.py --series <series.json> --text voiceover/vo_text.txt --style voiceover/style.txt --out voiceover/vo_full.wav
  options: --voice Sami --model gemini-3.8-flash-tts --temperature 1.0 --seed 20261024 --language th-TH
Seed rule (user, 2026-10-24): the seed locks the voice timbre. Takes with the same seed are not byte-identical and the
emotion differs a little each run, which is fine; the user only wants the same-sounding voice. So a series keeps the same
model, voice, seed, temperature (series.json voice.temperature; with a locked seed the user wants the normal 1.0), API path and style_base for
every episode, and the voice is NOT converted with Seed-VC afterwards.
The API's Sami sounds different from the web UI's Sami: never switch between web and API inside one series.
Voice gender (2026-10-24): in the API "Sami" = id en-us-sami, a FEMALE voice. A style that asks for a man fights the voice and the
gender flips from take to take. Pick a voice whose own gender matches the narrator (GET /v1beta/voices lists id, gender, pitch, persona);
แทรกซึม uses en-us-storyteller-14 (male, 28, low).
           --api interactions|generate   (interactions = documented speech API with style; generate = generateContent)
           --dry-run                     (print the request body, call nothing)

API key: read from the environment variable GEMINI_API_KEY. Create it yourself in AI Studio (Get API key) and set it in
your own shell; it is never printed, logged, or written anywhere by this tool.

Notes
- Gemini 3.8 TTS reads `text` as a verbatim transcript: style goes in a speech_metadata annotation (Interactions API),
  never inside the text (it would be spoken).
- The Interactions API documents `seed`; temperature is sent in the same generation_config. If the service rejects a
  field, the error is printed and you can retry with --api generate (generateContent supports temperature and seed,
  but has no documented style field, so style is dropped there with a warning).
- Output: 24 kHz mono 16-bit WAV.
"""
import argparse, base64, json, os, struct, sys, urllib.error, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://generativelanguage.googleapis.com/v1beta"


def wav_bytes(pcm, rate=24000, ch=1, bits=16):
    size = len(pcm)
    return struct.pack("<4sI4s4sIHHIIHH4sI", b"RIFF", 36 + size, b"WAVE", b"fmt ", 16, 1, ch, rate, rate * ch * bits // 8, ch * bits // 8, bits, b"data", size) + pcm


def find_audio(obj):
    """Walk any response shape and return (bytes, mime) of the first audio payload."""
    if isinstance(obj, dict):
        mime = obj.get("mime_type") or obj.get("mimeType") or ""
        data = obj.get("data")
        if data and (mime.startswith("audio") or obj.get("type") == "audio"):
            return base64.b64decode(data), mime
        for v in obj.values():
            r = find_audio(v)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_audio(v)
            if r:
                return r
    return None


def body_interactions(a, text, style):
    # shape from the official REST example: input = [user_input{content: [text + speech_metadata annotation]}]
    item = {"type": "text", "text": text}
    if style:
        item["annotations"] = [{"type": "speech_metadata", "style": style}]
    spk = {"voice": a.voice}
    if a.language:
        spk["language"] = a.language
    gen = {"speech_config": [spk]}
    if a.seed is not None:
        gen["seed"] = a.seed
    if a.temperature is not None:
        gen["temperature"] = a.temperature
    return {"model": a.model, "input": [{"type": "user_input", "content": [item]}], "response_format": {"type": "audio"}, "generation_config": gen}


def body_generate(a, text, style):
    if style:
        print("warning: generateContent has no documented style field; style is not sent", file=sys.stderr)
    return {"contents": [{"role": "user", "parts": [{"text": text}]}],
            "generationConfig": {"temperature": a.temperature, "seed": a.seed, "responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": a.voice}}}}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series"); ap.add_argument("--text", required=True); ap.add_argument("--style"); ap.add_argument("--out", required=True)
    ap.add_argument("--voice"); ap.add_argument("--model"); ap.add_argument("--temperature", type=float); ap.add_argument("--seed", type=int)
    ap.add_argument("--language"); ap.add_argument("--api", choices=["interactions", "generate"], default="interactions"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    cfg = json.load(open(a.series, encoding="utf-8")).get("voice", {}) if a.series else {}
    a.voice = a.voice or cfg.get("voice", "Sami")
    a.model = a.model or cfg.get("model", "gemini-3.8-flash-tts")
    a.temperature = a.temperature if a.temperature is not None else cfg.get("temperature", 1.0)
    a.seed = a.seed if a.seed is not None else cfg.get("seed", 20261024)
    a.language = a.language or cfg.get("language")
    text = open(a.text, encoding="utf-8").read().strip()
    if a.style and os.path.exists(a.style):
        style = open(a.style, encoding="utf-8").read().strip()
    else:
        style = a.style or cfg.get("style_base", "")
    if a.api == "interactions":
        url, body = f"{BASE}/interactions", body_interactions(a, text, style)
    else:
        url, body = f"{BASE}/models/{a.model}:generateContent", body_generate(a, text, style)
    print(f"model {a.model} | voice {a.voice} | temperature {a.temperature} | seed {a.seed} | api {a.api} | {len(text)} chars")
    if a.dry_run:
        print(json.dumps(body, ensure_ascii=False, indent=1)[:3000])
        return
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set. Create a key in AI Studio (Get API key) and set it in your own environment.")
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            resp = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:1500]}")
    found = find_audio(resp)
    if not found:
        sys.exit("no audio in the response: " + json.dumps(resp, ensure_ascii=False)[:1500])
    data, mime = found
    if not data[:4] == b"RIFF":
        rate = 24000
        for part in mime.split(";"):
            if part.strip().startswith("rate="):
                rate = int(part.strip()[5:])
        data = wav_bytes(data, rate)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "wb").write(data)
    print(f"written {a.out} ({len(data) / 48000:.1f} s at 24 kHz)")


if __name__ == "__main__":
    main()
