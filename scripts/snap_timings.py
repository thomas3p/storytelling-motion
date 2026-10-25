"""Snap ASR phrase boundaries to the nearest real pause in the voiceover.

usage: python snap_timings.py vo.wav timings_asr.json timings.json [--win 0.6]
Each boundary between phrase i and i+1 moves to the closest silence (>= 0.12 s, -38 dB)
within --win seconds: phrase i ends where the pause starts, i+1 starts where it ends.
Boundaries with no pause nearby keep the ASR time. Prints how far each one moved.
"""
import argparse, json, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("wav"); ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--win", type=float, default=0.6)
a = ap.parse_args()

log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.wav, "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
gaps = list(zip([float(x) for x in re.findall(r"silence_start: ([-\d.]+)", log)], [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]))
d = json.load(open(a.src, encoding="utf-8"))
P = d["phrases"]
if gaps and gaps[0][0] <= 0.05: P[0]["start"] = round(gaps[0][1], 3)
for i in range(len(P) - 1):
    b = (P[i]["end"] + P[i + 1]["start"]) / 2
    best = min(gaps, key=lambda g: abs((g[0] + g[1]) / 2 - b), default=None)
    if best and abs((best[0] + best[1]) / 2 - b) <= a.win and best[0] > P[i]["start"] + 0.15:
        P[i]["end"], P[i + 1]["start"] = round(best[0], 3), round(best[1], 3)
        moved = round((best[0] + best[1]) / 2 - b, 2)
    else:
        moved = None
    print(f'{P[i]["start"]:6.2f}-{P[i]["end"]:6.2f} moved={moved} {P[i]["text"]}')
print(f'{P[-1]["start"]:6.2f}-{P[-1]["end"]:6.2f} {P[-1]["text"]}')
secs = {}
for p in P:
    s = secs.setdefault(p["section"], {"start": p["start"], "end": p["end"]}); s["end"] = p["end"]
d["sections"] = secs
json.dump(d, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
