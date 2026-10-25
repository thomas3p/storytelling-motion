"""Time a known Thai script against a voiceover using faster-whisper word timestamps.

usage: python align_asr.py vo.wav captions.txt timings.json [--model medium]
captions.txt is the same format as align_script.py ("## section", "spoken || display").
Whisper's Thai text is not trusted as the caption: it only supplies a clock. The script's
characters are matched to the transcript's characters (difflib), and each phrase takes the
times of its first and last matched characters. Unmatched edges are filled from neighbours.
"""
import argparse, difflib, json, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")

ap = argparse.ArgumentParser()
ap.add_argument("wav"); ap.add_argument("script"); ap.add_argument("out")
ap.add_argument("--model", default="medium")
a = ap.parse_args()

def norm(t):
    return "".join(c for c in t if not c.isspace() and c not in "…ๆฯ.,!?\"'“”" and not unicodedata.category(c).startswith("P"))

phrases, section = [], None
for line in open(a.script, encoding="utf-8"):
    line = line.strip()
    if not line: continue
    if line.startswith("## "): section = line[3:]; continue
    spoken, _, shown = line.partition("||")
    phrases.append({"text": spoken.strip(), "display": (shown or spoken).strip(), "section": section})

from faster_whisper import WhisperModel
try:
    model = WhisperModel(a.model, device="cuda", compute_type="float16")
except Exception:
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
segs, info = model.transcribe(a.wav, language="th", word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
chars, times = [], []   # transcript chars with (start, end) per char
for s in segs:
    for w in s.words:
        t = norm(w.word)
        if not t: continue
        step = (w.end - w.start) / len(t)
        for k, c in enumerate(t):
            chars.append(c); times.append((w.start + k * step, w.start + (k + 1) * step))
asr = "".join(chars)

script = ""; owner = []
for i, p in enumerate(phrases):
    t = norm(p["text"]); script += t; owner += [i] * len(t)

sm = difflib.SequenceMatcher(None, script, asr, autojunk=False)
hit = {}
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        hit[blk.a + k] = blk.b + k
for i, p in enumerate(phrases):
    idx = [j for j, o in enumerate(owner) if o == i and j in hit]
    p["matched"] = round(len(idx) / max(1, owner.count(i)), 2)
    p["start"] = round(times[hit[idx[0]]][0], 3) if idx else None
    p["end"] = round(times[hit[idx[-1]]][1], 3) if idx else None
# fill gaps from neighbours, keep order
for i, p in enumerate(phrases):
    if p["start"] is None:
        p["start"] = phrases[i - 1]["end"] if i else 0.0
    if p["end"] is None:
        nxt = next((q["start"] for q in phrases[i + 1:] if q["start"] is not None), p["start"] + 1.0)
        p["end"] = nxt
for i in range(1, len(phrases)):
    if phrases[i]["start"] < phrases[i - 1]["end"]:
        phrases[i]["start"] = phrases[i - 1]["end"]
sections = {}
for p in phrases:
    s = sections.setdefault(p["section"], {"start": p["start"], "end": p["end"]}); s["end"] = p["end"]
json.dump({"duration": info.duration, "engine": f"faster-whisper {a.model}", "asr_text": asr, "sections": sections, "phrases": phrases},
          open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for p in phrases:
    print(f'{p["start"]:6.2f}-{p["end"]:6.2f} m={p["matched"]:.2f} {p["text"]}')
print("overall match:", round(sm.ratio(), 3))
