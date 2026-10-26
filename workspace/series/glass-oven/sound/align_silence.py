"""Time a one-take voiceover against its script without speech recognition: find the pauses, then pick the phrase boundaries that
best match where each phrase should end (by its share of the script's characters), preferring longer pauses.

usage: python align_silence.py vo.wav captions.txt timings_final.json [--min-gap 0.15] [--db -38]
captions.txt: "## section" lines and "spoken || display" lines (tools/align_asr.py format). Writes the timings_final.json format
scenekit reads. Check the printed table against the audio: a phrase the model skipped or added shifts every boundary after it.
"""
import argparse, json, re
import numpy as np, soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("wav"); ap.add_argument("script"); ap.add_argument("out")
ap.add_argument("--min-gap", type=float, default=0.15); ap.add_argument("--db", type=float, default=-38)
a = ap.parse_args()

phrases, section = [], None
for line in open(a.script, encoding="utf-8"):
    line = line.strip()
    if not line: continue
    if line.startswith("##"): section = line[2:].strip(); continue
    spoken, _, display = line.partition(" || ")
    phrases.append({"text": spoken.strip(), "display": (display or spoken).strip(), "section": section})

x, sr = sf.read(a.wav, dtype="float32")
if x.ndim > 1: x = x.mean(axis=1)
hop = int(0.01 * sr)
rms = np.sqrt(np.convolve(x ** 2, np.ones(hop * 2) / (hop * 2), mode="same")[::hop] + 1e-12)
db = 20 * np.log10(rms / (rms.max() + 1e-12))
voiced = db > a.db
idx = np.flatnonzero(voiced)
t0, t1 = idx[0] * 0.01, (idx[-1] + 1) * 0.01
gaps, i = [], idx[0]
while i < idx[-1]:
    if not voiced[i]:
        j = i
        while j < len(voiced) and not voiced[j]: j += 1
        if (j - i) * 0.01 >= a.min_gap: gaps.append((i * 0.01, j * 0.01))
        i = j
    else:
        i += 1
n = len(phrases)
if len(gaps) < n - 1:
    raise SystemExit(f"only {len(gaps)} pauses for {n} phrases — lower --min-gap or --db")
w = np.array([len(re.sub(r"\s|…", "", p["text"])) for p in phrases], float)
speech = (t1 - t0) - sum(b - a_ for a_, b in gaps) * 0.5
expect = t0 + np.cumsum(w)[:-1] / w.sum() * (t1 - t0)
# DP: boundary k (0..n-2) takes gap g, gaps strictly increasing; cost = distance to the expected time − bonus for long pauses
G = len(gaps); mid = np.array([(g[0] + g[1]) / 2 for g in gaps]); ln = np.array([g[1] - g[0] for g in gaps])
INF = 1e18; cost = np.full((n - 1, G), INF); back = np.zeros((n - 1, G), int)
for g in range(G):
    cost[0, g] = abs(mid[g] - expect[0]) - 1.5 * ln[g]
for k in range(1, n - 1):
    best, arg = INF, -1
    for g in range(G):
        if g - 1 >= 0 and cost[k - 1, g - 1] < best: best, arg = cost[k - 1, g - 1], g - 1
        if arg >= 0: cost[k, g] = best + abs(mid[g] - expect[k]) - 1.5 * ln[g]; back[k, g] = arg
g = int(np.argmin(cost[n - 2])); pick = [g]
for k in range(n - 2, 0, -1):
    g = back[k, g]; pick.append(g)
pick = pick[::-1]
starts = [t0] + [gaps[g][1] for g in pick]; ends = [gaps[g][0] for g in pick] + [t1]
for p, s, e in zip(phrases, starts, ends):
    p["start"], p["end"] = round(s, 3), round(e, 3)
secs = {}
for p in phrases:
    s = secs.setdefault(p["section"], {"start": p["start"], "end": p["end"]}); s["end"] = p["end"]
json.dump({"duration": round(len(x) / sr, 3), "engine": "align_silence (pauses + character share, no ASR)", "sections": secs, "phrases": phrases},
          open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, p in enumerate(phrases):
    print(f'{k:2d} {p["start"]:6.2f}-{p["end"]:6.2f} {p["section"]:7} {p["text"]}')
