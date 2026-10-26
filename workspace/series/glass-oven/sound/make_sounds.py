"""Synthesize the sound effects and music beds of 60°C รุ่งอรุณเดือด (no samples, no third-party licences: every file is made
here from sine waves and filtered noise with a fixed random seed, so a re-run gives the same files).

usage: python make_sounds.py <hf/assets folder>      writes sfx/*.wav and bgm/*.wav (48 kHz mono)
"""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
rng = np.random.default_rng(20261026)


def t_(d):
    return np.arange(int(d * SR)) / SR


def noise(d):
    return rng.standard_normal(int(d * SR))


def filt(x, kind, f, order=4):
    f = np.atleast_1d(f) / (SR / 2)
    return sosfilt(butter(order, f if len(f) > 1 else f[0], btype=kind, output="sos"), x)


def env(d, a=0.01, r=0.2, sustain=1.0):
    n = int(d * SR); e = np.full(n, sustain)
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, sustain, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def decay(d, tau):
    return np.exp(-t_(d) / tau)


def sweep(f0, f1, d, curve="exp"):
    t = t_(d)
    f = f0 * (f1 / f0) ** (t / d) if curve == "exp" else f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def reverb(x, size=1.6, mix=0.25):
    ir = noise(size) * decay(size, size / 5)
    ir = filt(ir, "lowpass", 5000) / np.sqrt(np.sum(ir ** 2))
    wet = fftconvolve(x, ir)[: len(x) + int(size * SR)]
    out = np.concatenate([x, np.zeros(len(wet) - len(x))])
    return out * (1 - mix) + wet * mix


def pad_to(x, d):
    n = int(d * SR)
    return np.concatenate([x, np.zeros(max(0, n - len(x)))])[:n]


def mix(*parts):
    n = max(len(p) for p in parts)
    return sum(np.concatenate([p, np.zeros(n - len(p))]) for p in parts)


def at(x, sec, total):
    out = np.zeros(int(total * SR)); i = int(sec * SR)
    out[i: i + len(x)] += x[: max(0, len(out) - i)]
    return out


def norm(x, peak=0.89):
    return x / max(1e-9, np.abs(x).max()) * peak


# ── music beds ─────────────────────────────────────────────────────────
def heat_drone(d=95):
    t = t_(d)
    tone = sum(a * np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.07 * t * (i + 1)))
               for i, (f, a) in enumerate([(55, 0.5), (55.4, 0.4), (82.4, 0.3), (110, 0.22), (164.8, 0.1), (220.6, 0.06)]))
    shimmer = filt(noise(d), "bandpass", [2200, 5200]) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.11 * t)) * 0.05
    swell = 0.6 + 0.4 * np.sin(2 * np.pi * t / 23 - 1.5)
    return norm(reverb((tone * swell + shimmer) * env(d, 3, 4), 2.5, 0.3)[: int(d * SR)], 0.7)


def dark_drone(d=30):
    t = t_(d)
    tone = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(36.7, 0.6), (37.1, 0.5), (73.4, 0.3), (87.3, 0.18), (103.8, 0.12)])
    rumble = filt(noise(d), "lowpass", 90) * 0.6
    beat = 0.7 + 0.3 * np.sin(2 * np.pi * 0.25 * t)
    return norm(reverb((tone + rumble) * beat * env(d, 2, 3), 2.0, 0.3)[: int(d * SR)], 0.75)


def thump(f0=90, f1=38, d=0.35, click=0.3):
    x = sweep(f0, f1, d) * decay(d, d / 4)
    c = filt(noise(0.02), "highpass", 1500) * click * decay(0.02, 0.005)
    return mix(x, c)


def pulse(d=45, bpm=100):
    out = np.zeros(int(d * SR)); beat = 60 / bpm
    for k in range(int(d / beat)):
        out = mix(out, at(thump(80, 40, 0.3, 0.15) * (1.0 if k % 2 == 0 else 0.6), k * beat, d))
    return norm(reverb(out * env(d, 1, 2), 0.8, 0.2)[: int(d * SR)], 0.8)


def heartbeat(d=14, bpm=72):
    out = np.zeros(int(d * SR)); beat = 60 / bpm
    for k in range(int(d / beat)):
        out = mix(out, at(thump(70, 35, 0.22, 0.05), k * beat, d), at(thump(60, 32, 0.2, 0.03) * 0.7, k * beat + 0.28, d))
    return norm(filt(out, "lowpass", 400), 0.9)


# ── effects ────────────────────────────────────────────────────────────
def hot_wind(d=14):
    t = t_(d)
    x = filt(np.cumsum(noise(d)) * 0.02, "bandpass", [80, 900])
    gust = 0.45 + 0.55 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.61 * t + 1))
    return norm(x * gust * env(d, 1.5, 2), 0.7)


def beep(d=0.4, f=1320):
    x = (np.sin(2 * np.pi * f * t_(d)) + 0.25 * np.sin(2 * np.pi * 2 * f * t_(d))) * env(d, 0.005, 0.25)
    return norm(reverb(x, 0.6, 0.2), 0.6)


def riser(d=1.6):
    x = sweep(160, 1800, d) * 0.5 + filt(noise(d), "bandpass", [600, 6000]) * 0.4
    return norm(x * np.linspace(0, 1, len(x)) ** 2 * env(d, 0.01, 0.05), 0.8)


def impact(d=2.6):
    boom = sweep(70, 26, d) * decay(d, 0.45)
    hit = filt(noise(0.4), "lowpass", 1200) * decay(0.4, 0.06)
    return norm(reverb(mix(boom, hit * 0.8), 2.2, 0.35)[: int(d * SR)], 0.95)


def swell(d=2.8):
    x = filt(noise(d), "highpass", 2500) * 0.6 + sum(np.sin(2 * np.pi * f * t_(d)) * 0.15 for f in (440, 660, 880))
    return norm(x * np.linspace(0, 1, len(x)) ** 2.5 * env(d, 0.01, 0.12), 0.7)


def whoosh(d=1.2):
    n = len(t_(d)); x = noise(d); out = np.zeros(n); seg = 2400
    for i in range(0, n, seg):
        k = i / n; fc = 300 + 3000 * np.sin(np.pi * k)
        out[i: i + seg] = filt(x[i: i + seg + 2000], "bandpass", [fc * 0.6, fc * 1.4], 2)[:len(out[i: i + seg])]
    return norm(out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5, 0.7)


def ac_hum(d=16):
    t = t_(d)
    hum = sum(a * np.sin(2 * np.pi * f * t) for f, a in [(50, 0.4), (100, 0.3), (150, 0.12), (200, 0.08)])
    fan = filt(noise(d), "bandpass", [250, 900]) * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * t)) * 0.5
    rattle = filt(noise(d), "bandpass", [1800, 3200]) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 11 * t))) * 0.06
    return norm((hum + fan + rattle) * env(d, 0.4, 0.4), 0.7)


def news_chime(d=1.8):
    out = np.zeros(int(d * SR))
    for k, f in enumerate([659.3, 1046.5, 784.0]):
        tt = t_(0.9)
        out = mix(out, at((np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * decay(0.9, 0.25), k * 0.18, d))
    return norm(reverb(out, 1.0, 0.25)[: int(d * SR)], 0.7)


def glitch(d=0.6):
    n = int(d * SR); out = np.zeros(n); i = 0
    while i < n:
        L = int(rng.uniform(0.01, 0.05) * SR)
        f = rng.choice([180, 440, 880, 1500, 3000])
        seg = np.sign(np.sin(2 * np.pi * f * np.arange(L) / SR)) * 0.5 if rng.random() > 0.4 else rng.standard_normal(L) * 0.4
        out[i: i + L] = seg[: len(out[i: i + L])] * (rng.random() > 0.25)
        i += L
    return norm(filt(out, "lowpass", 7000) * env(d, 0.002, 0.08), 0.7)


def explosion(d=2.4):
    body = filt(noise(d), "lowpass", 2400) * decay(d, 0.35)
    low = filt(noise(d), "lowpass", 160) * decay(d, 0.6) * 2.0
    sub = sweep(60, 25, d) * decay(d, 0.5) * 0.9
    crack = np.zeros(int(d * SR))
    for _ in range(40):
        s = rng.uniform(0.05, 1.6); L = int(0.004 * SR); i = int(s * SR)
        crack[i: i + L] += noise(0.004) * rng.uniform(0.2, 0.6) * np.exp(-s * 1.5)
    x = mix(body, low, sub, filt(crack, "highpass", 1500))
    x[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    return norm(reverb(np.tanh(x * 1.5), 1.8, 0.3)[: int(d * SR)], 0.95)


def tick(d=16, rate=2.0):
    out = np.zeros(int(d * SR))
    for k in range(int(d * rate)):
        c = filt(noise(0.015), "bandpass", [2000, 6000]) * decay(0.015, 0.003) * (1.0 if k % 2 == 0 else 0.7)
        out = mix(out, at(c, k / rate, d))
    return norm(out, 0.6)


def boil(d=10):
    out = filt(noise(d), "lowpass", 300) * 0.3 * env(d, 0.5, 0.5)
    for _ in range(int(d * 45)):
        s = rng.uniform(0, d - 0.1); L = rng.uniform(0.02, 0.06); f0 = rng.uniform(300, 900)
        b = sweep(f0, f0 * rng.uniform(1.5, 2.5), L) * decay(L, L / 3) * rng.uniform(0.2, 0.6)
        out = mix(out, at(b, s, d))
    hiss = filt(noise(d), "highpass", 4000) * 0.08
    return norm(reverb(out + hiss, 0.5, 0.15)[: int(d * SR)], 0.75)


def flutter(d=2.4):
    t = t_(d)
    x = filt(noise(d), "bandpass", [300, 2500]) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 13 * t))) * decay(d, 0.8)
    return norm(x * env(d, 0.02, 0.3), 0.6)


def thud(d=1.4):
    x = at(thump(120, 50, 0.25, 0.2), 0.0, d) + at(thump(110, 45, 0.25, 0.15) * 0.6, 0.42, d) + at(thump(130, 55, 0.2, 0.1) * 0.4, 0.75, d)
    return norm(filt(x, "lowpass", 900), 0.8)


def power_down(d=2.0):
    click = filt(noise(0.03), "highpass", 800) * decay(0.03, 0.008)
    down = sweep(420, 35, d - 0.1) * np.linspace(1, 0, int((d - 0.1) * SR)) ** 1.5
    hum = (np.sin(2 * np.pi * 100 * t_(d)) * 0.3) * np.linspace(1, 0, int(d * SR)) ** 3
    return norm(mix(click, at(down, 0.08, d), hum), 0.85)


def alarm(d=14):
    out = np.zeros(int(d * SR))
    for k in range(int(d / 0.5)):
        f = 780 if k % 2 == 0 else 620; tt = t_(0.42)
        out = mix(out, at(np.sign(np.sin(2 * np.pi * f * tt)) * 0.3 * env(0.42, 0.01, 0.05), k * 0.5, d))
    return norm(filt(reverb(out, 1.2, 0.35)[: int(d * SR)], "lowpass", 2500), 0.6)


def door(d=1.4):
    push = filt(noise(0.8), "bandpass", [120, 700]) * np.sin(np.pi * np.linspace(0, 1, int(0.8 * SR))) * 0.6
    creak = sweep(180, 240, 0.6) * 0.15 * np.sin(np.pi * np.linspace(0, 1, int(0.6 * SR)))
    latch = filt(noise(0.05), "highpass", 1200) * decay(0.05, 0.01)
    return norm(reverb(mix(latch, at(push, 0.05, d), at(creak, 0.2, d)), 1.0, 0.3)[: int(d * SR)], 0.8)


def intercom_buzz(d=1.0):
    out = np.zeros(int(d * SR))
    for s in (0.0, 0.42):
        tt = t_(0.3)
        out = mix(out, at(np.tanh(3 * np.sign(np.sin(2 * np.pi * 410 * tt)) * 0.4) * env(0.3, 0.005, 0.03), s, d))
    return norm(filt(out, "bandpass", [300, 3400]), 0.7)


def static(d=2.0):
    x = filt(noise(d), "bandpass", [300, 3400]) * 0.4
    for _ in range(60):
        s = rng.uniform(0, d - 0.01); x = mix(x, at(noise(0.006) * rng.uniform(0.5, 1.2), s, d))
    return norm(filt(x, "bandpass", [250, 4000]) * env(d, 0.03, 0.2), 0.6)


SOUNDS = {
    "bgm/heat_drone.wav": heat_drone, "bgm/dark_drone.wav": dark_drone, "bgm/pulse.wav": pulse,
    "sfx/hot_wind.wav": hot_wind, "sfx/beep.wav": beep, "sfx/riser.wav": riser, "sfx/impact.wav": impact, "sfx/swell.wav": swell,
    "sfx/whoosh.wav": whoosh, "sfx/ac_hum.wav": ac_hum, "sfx/news_chime.wav": news_chime, "sfx/glitch.wav": glitch, "sfx/explosion.wav": explosion,
    "sfx/tick.wav": tick, "sfx/boil.wav": boil, "sfx/flutter.wav": flutter, "sfx/thud.wav": thud, "sfx/power_down.wav": power_down,
    "sfx/alarm.wav": alarm, "sfx/door.wav": door, "sfx/intercom_buzz.wav": intercom_buzz, "sfx/static.wav": static, "sfx/heartbeat.wav": heartbeat,
}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    for name, fn in SOUNDS.items():
        out = os.path.join(sys.argv[1], name)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        x = fn()
        sf.write(out, np.clip(x, -1, 1).astype(np.float32), SR, subtype="PCM_16")
        print(f"{name:28} {len(x) / SR:6.2f}s")
