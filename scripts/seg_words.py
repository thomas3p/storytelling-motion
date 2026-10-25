"""Transcribe a segment of a wav with faster-whisper and print word timings (absolute seconds)."""
import sys, subprocess, tempfile, os
from faster_whisper import WhisperModel
sys.stdout.reconfigure(encoding="utf-8")
wav, t0, dur = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
tmp = os.path.join(tempfile.gettempdir(), "segw.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-t", str(dur), "-i", wav, "-ar", "16000", "-ac", "1", tmp], check=True)
m = WhisperModel("medium", device="cuda", compute_type="float16")
segs, _ = m.transcribe(tmp, language="th", word_timestamps=True)
for s in segs:
    print(f"[{s.start + t0:6.2f}-{s.end + t0:6.2f}] {s.text}")
    print("   " + " ".join(f"{w.word.strip()}@{w.start + t0:.2f}" for w in s.words))
