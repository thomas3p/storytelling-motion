"""Shorten long pauses in a voiceover WAV (same take, so the voice stays consistent).

usage: python tighten_vo.py in.wav out.wav [--keep 0.4] [--min 0.5] [--db -35]
Every silence longer than --min seconds is cut down to --keep seconds (half kept at each edge).
Prints a JSON map of old->new times for the kept speech chunks.
"""
import argparse, json, re, subprocess, sys, wave
sys.stdout.reconfigure(encoding="utf-8")

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--keep", type=float, default=0.4)
ap.add_argument("--min", type=float, default=0.5)
ap.add_argument("--db", type=float, default=-35)
a = ap.parse_args()

log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.src, "-af",
                      f"silencedetect=noise={a.db}dB:d={a.min}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]

with wave.open(a.src, "rb") as w:
    params = w.getparams(); sr = w.getframerate(); bpf = w.getsampwidth() * w.getnchannels()
    data = w.readframes(w.getnframes())
total = len(data) / bpf / sr

cuts = []  # (cut_from, cut_to) in seconds
for s, e in zip(starts, ends):
    if e - s > a.keep:
        cuts.append((s + a.keep / 2, e - a.keep / 2))

out, pos, chunks, removed = bytearray(), 0.0, [], 0.0
for cf, ct in cuts + [(total, total)]:
    out += data[int(pos * sr) * bpf:int(cf * sr) * bpf]
    chunks.append({"src_start": round(pos, 3), "src_end": round(cf, 3), "dst_start": round(pos - removed, 3)})
    removed += ct - cf; pos = ct

with wave.open(a.dst, "wb") as w:
    w.setparams(params); w.writeframes(bytes(out))
print(json.dumps({"src_duration": round(total, 3), "dst_duration": round(len(out) / bpf / sr, 3), "chunks": chunks}, ensure_ascii=False))
