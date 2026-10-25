"""Insert silent beats into a voiceover after given phrases and shift the timings to match.

usage: python insert_gaps.py vo.wav timings.json out.wav out_timings.json 16:0.6 17:1.2 ...
"16:0.6" = 0.6 s of silence after phrase 16 (index in timings.json), placed mid-pause.
"""
import json, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
wav, src, out_wav, out_json, *specs = sys.argv[1:]
d = json.load(open(src, encoding="utf-8"))
P = d["phrases"]
gaps = sorted((int(i), float(s)) for i, s in (x.split(":") for x in specs))
cuts = []  # (time in the original file, seconds)
for i, sec in gaps:
    t = round((P[i]["end"] + P[i + 1]["start"]) / 2, 3) if i + 1 < len(P) else round(P[i]["end"] + 0.05, 3)
    cuts.append((t, sec))
# shift phrase times (later phrases move by every gap placed before them)
for p in P:
    shift = sum(sec for t, sec in cuts if t <= p["start"])
    p["start"] = round(p["start"] + shift, 3); p["end"] = round(p["end"] + shift, 3)
d["inserted_gaps"] = [{"at": t, "seconds": s} for t, s in cuts]
d["duration"] = round(d.get("duration", 0) + sum(s for _, s in cuts), 3)
secs = {}
for p in P:
    s = secs.setdefault(p["section"], {"start": p["start"], "end": p["end"]}); s["end"] = p["end"]
d["sections"] = secs
json.dump(d, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# audio: split at each cut and splice in silence
parts, chain, prev = [], [], 0.0
for k, (t, sec) in enumerate(cuts):
    parts.append(f"[0]atrim={prev}:{t},asetpts=N/SR/TB[a{k}]")
    parts.append(f"anullsrc=r=48000:cl=mono,atrim=0:{sec}[s{k}]")
    chain += [f"[a{k}]", f"[s{k}]"]
    prev = t
parts.append(f"[0]atrim={prev},asetpts=N/SR/TB[z]"); chain.append("[z]")
fc = ";".join(parts) + ";" + "".join(chain) + f"concat=n={len(chain)}:v=0:a=1"
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", wav, "-filter_complex", fc, "-ar", "48000", "-ac", "1", out_wav], check=True)
print("gaps", cuts, "->", d["duration"])
