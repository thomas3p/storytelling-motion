"""Make phrases of a voiceover sound like they come through the intercom (telephone band, light overdrive, a little echo).

usage: python vo_intercom.py vo_in.wav timings_final.json vo_out.wav 17 [18 ...]   (phrase indexes)
"""
import json, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

src, tim, out, *idx = sys.argv[1:]
x, sr = sf.read(src, dtype="float32")
P = json.load(open(tim, encoding="utf-8"))["phrases"]
for i in map(int, idx):
    a, b = int((P[i]["start"] - 0.05) * sr), int((P[i]["end"] + 0.25) * sr)
    seg = x[a:b].copy()
    seg = sosfilt(butter(4, [380 / (sr / 2), 3000 / (sr / 2)], btype="bandpass", output="sos"), seg)
    seg = np.tanh(seg * 4.0) * 0.5
    d = int(0.09 * sr); echo = np.concatenate([np.zeros(d), seg[:-d]]) * 0.3
    seg = seg + echo
    fade = np.minimum(1, np.minimum(np.arange(len(seg)), np.arange(len(seg))[::-1]) / (0.02 * sr))
    x[a:b] = x[a:b] * (1 - fade) + seg * fade
sf.write(out, x, sr)
print("intercom fx on phrases", idx)
