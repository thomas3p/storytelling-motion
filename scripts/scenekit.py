"""Modular scene pipeline for HyperFrames storytelling clips.

One file per scene, a timeline written in voiceover cues (not seconds), and audio + captions placed by the same cues,
so several agents can each own a scene file in parallel, and a new or external voiceover only needs re-aligning.

Episode layout (inside hf/):
  timeline.json
    {
      "series_lib": "../../../series/<slug>/lib",          (folder with looks.py, sets.py, hud.py)
      "duration": "p19.end+2.0",
      "cues": { "title": "p1-0.2" },                       (optional named cues, usable anywhere)
      "scenes": [ { "id": "s01", "module": "s01_hook", "start": "0" }, { "id": "s02", "module": "s02_office", "start": "p2-0.3" }, ... ],
      "audio": [ { "id": "vo", "src": "audio/vo.wav", "at": "0", "dur": "file", "track": 10 },
                 { "id": "sfx-door", "src": "sfx/door.mp3", "at": "p5.end+0.1", "dur": 1.2, "vol": 0.6, "fi": 0, "fo": 0.2, "ms": 0, "track": 15 } ],
      "captions": { "skip": [14], "last_until": "end-0.3", "hl": { "word": "#hex" },
                    "overrides": { "8": { "shift": 0.1, "hold": 0.4, "text": "display text", "hide": false } } }
    }
  scenes/<module>.py   SCENE = {"title": "..."}  and  def build(ctx) -> str  (return ctx.scene(css, svg, overlays, js))
  ../voiceover/timings_final.json   phrases from tools/align_* + insert_gaps (any external VO: align it, run build again)

Cue grammar: "p7" (start of phrase 7), "p7.end", "s03" (start of scene s03), "<named cue>", "end" (film end), "12.5",
each optionally followed by +/- seconds: "p7.end+0.25", "s04-0.5".

In a scene module, ctx gives:
  ctx.sid, ctx.dur, ctx.start      scene id, length, absolute start
  ctx.t("p8")                       local time (seconds from this scene's start) of any cue
  ctx.lib.looks / .sets / .hud      the series library
  ctx.scene(css, svg, overlays, js, bg)   wraps personkit.scene with the series HUD css included
Run:  python hf/build.py    (writes compositions/*.html, compositions/captions.html, index.html, timeline_resolved.json)
"""
import importlib.util, json, os, re, subprocess, sys
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from personkit import scene as pk_scene, write
from flatkit import scene as fk_scene

CUE = re.compile(r"^\s*([A-Za-z_][\w.]*|[\d.]+)\s*(([+-])\s*([\d.]+))?\s*$")


class Timeline:
    def __init__(self, hf):
        self.hf = hf
        self.cfg = json.load(open(os.path.join(hf, "timeline.json"), encoding="utf-8"))
        tf = json.load(open(os.path.join(hf, "..", "voiceover", "timings_final.json"), encoding="utf-8"))
        self.phr = tf["phrases"]
        self.named = self.cfg.get("cues", {})
        self.scene_start = {}
        self.end = None
        self.end = self.resolve(self.cfg["duration"])
        for s in self.cfg["scenes"]:
            self.scene_start[s["id"]] = round(self.resolve(s["start"]), 3)

    def resolve(self, expr):
        if isinstance(expr, (int, float)):
            return float(expr)
        m = CUE.match(str(expr))
        if not m:
            raise ValueError(f"bad cue: {expr}")
        base, off = m.group(1), (float(m.group(4)) * (1 if m.group(3) == "+" else -1) if m.group(2) else 0.0)
        if re.fullmatch(r"[\d.]+", base):
            v = float(base)
        elif base == "end":
            if self.end is None:
                raise ValueError("'end' used before the duration is known")
            v = self.end
        elif base in self.named:
            v = self.resolve(self.named[base])
        elif re.fullmatch(r"p\d+(\.start|\.end)?", base):
            i, part = (base.split(".") + ["start"])[:2]
            v = self.phr[int(i[1:])]["start" if part == "start" else "end"]
        elif base in self.scene_start:
            v = self.scene_start[base]
        else:
            raise ValueError(f"unknown cue: {expr}")
        return v + off


class Ctx:
    def __init__(self, tl, sid, start, dur, lib, hud_css, fade=0.0):
        self.tl, self.sid, self.start, self.dur, self.lib, self._hud, self.fade = tl, sid, start, dur, lib, hud_css, fade

    def t(self, cue, off=0.0):
        return round(self.tl.resolve(cue) - self.start + off, 3)

    def scene(self, css, svg, overlays, js, bg="#0b0d14", **kw):
        if getattr(getattr(self.lib, "hud", None), "KIT", "person") == "flat":
            return fk_scene(self.sid, self.dur, self._hud + css, svg, overlays, js, bg, fade_in=self.fade, **kw)
        return pk_scene(self.sid, self.dur, self._hud + css, svg, overlays, js, bg)


def load_lib(path):
    lib = type("Lib", (), {})()
    for name in ("looks", "sets", "hud"):
        f = os.path.join(path, name + ".py")
        if os.path.exists(f):
            spec = importlib.util.spec_from_file_location(f"serieslib_{name}", f)
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            setattr(lib, name, mod)
    return lib


def build_episode(hf, title):
    tl = Timeline(hf)
    cfg = tl.cfg
    lib = load_lib(os.path.normpath(os.path.join(hf, cfg["series_lib"])))
    hud_css = getattr(getattr(lib, "hud", None), "CSS", "")
    DUR = round(tl.end, 2)
    scenes, resolved = cfg["scenes"], {"duration": DUR, "scenes": [], "phrases": [[round(p["start"], 3), round(p["end"], 3), p["text"]] for p in tl.phr]}
    hosts = []
    os.makedirs(os.path.join(hf, "compositions"), exist_ok=True)
    # "xfade": each scene runs on for xfade s under the next one, which fades in on top (alternate tracks, rising z-index)
    xf = float(cfg.get("xfade", 0))
    for k, s in enumerate(scenes):
        start = tl.scene_start[s["id"]]
        end = tl.scene_start[scenes[k + 1]["id"]] if k + 1 < len(scenes) else DUR
        dur = round(end - start + (xf if k + 1 < len(scenes) else 0), 3)
        spec = importlib.util.spec_from_file_location(f"scene_{s['module']}", os.path.join(hf, "scenes", s["module"] + ".py"))
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        html = mod.build(Ctx(tl, s["id"], start, dur, lib, hud_css, fade=(xf if k else 0.0)))
        name = f"{s['id']}-{s['module'].split('_', 1)[-1]}"
        write(os.path.join(hf, "compositions", name + ".html"), html)
        track = (1 if k % 2 == 0 else 3) if xf else 1
        hosts.append(f'      <div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{name}.html" data-start="{start}" data-duration="{dur}" data-track-index="{track}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {k + 1}"></div>')
        resolved["scenes"].append({"id": s["id"], "module": s["module"], "start": start, "end": end, "dur": dur,
                                   "phrases_inside": [i for i, p in enumerate(tl.phr) if start <= p["start"] < end]})
    # global overlays that span several scenes (EP tag …): "globals": [{ "id": "g01", "module": "g_ep", "start": "p2", "end": "p15.end" }]
    for g in cfg.get("globals", []):
        start = round(tl.resolve(g["start"]), 3); dur = round(tl.resolve(g["end"]) - start, 3)
        spec = importlib.util.spec_from_file_location(f"scene_{g['module']}", os.path.join(hf, "scenes", g["module"] + ".py"))
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        html = mod.build(Ctx(tl, g["id"], start, dur, lib, hud_css))
        name = f"{g['id']}-{g['module'].split('_', 1)[-1]}"
        write(os.path.join(hf, "compositions", name + ".html"), html)
        hosts.append(f'      <div id="{g["id"]}" data-composition-id="{g["id"]}" data-composition-src="compositions/{name}.html" data-start="{start}" data-duration="{dur}" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 90"></div>')
    # audio, placed by cues
    auds = []
    for a in cfg.get("audio", []):
        at = round(tl.resolve(a["at"]), 3)
        d = a.get("dur", "file")
        if d == "file":
            src = os.path.join(hf, "assets", a["src"])
            if os.path.exists(src):
                d = round(sf.info(src).duration, 2)
            else:  # media not downloaded yet (e.g. a shared example): run to the film end so the build still previews
                print(f"note: {a['src']} is missing, using the film length for its duration")
                d = round(tl.end - at, 3)
        elif isinstance(d, str):
            d = round(tl.resolve(d) - at, 3)
        x = f'      <audio id="{a["id"]}" class="clip" src="assets/{a["src"]}" data-start="{at}" data-duration="{d}" data-track-index="{a.get("track", 15)}" data-volume="{a.get("vol", 1)}"'
        if a.get("ms") is not None: x += f' data-media-start="{a["ms"]}"'
        if a.get("fi"): x += f' data-fade-in="{a["fi"]}"'
        if a.get("fo"): x += f' data-fade-out="{a["fo"]}"'
        auds.append(x + "></audio>")
    # captions, timed from the same alignment (with per-phrase overrides)
    cap = cfg.get("captions", {})
    ov_path = os.path.join(hf, "compositions", "_caption_overrides.json")
    json.dump(cap.get("overrides", {}), open(ov_path, "w", encoding="utf-8"), ensure_ascii=False)
    cmd = [sys.executable, "-I", os.path.join(HERE, "build_captions.py"), os.path.join(hf, "..", "voiceover", "timings_final.json"), os.path.join(hf, "compositions", "captions.html"),
           "--overrides", ov_path, "--last-until", str(round(tl.resolve(cap.get("last_until", "end-0.3")), 2))]
    if cap.get("skip"): cmd += ["--skip", ",".join(str(i) for i in cap["skip"])]
    if cap.get("hl"): cmd += ["--hl"] + [f"{w}={c}" for w, c in cap["hl"].items()]
    for key in ("style", "top", "size"):
        if cap.get(key) is not None: cmd += [f"--{key}", str(cap[key])]
    subprocess.run(cmd, check=True)
    idx = f'''<!doctype html>
<html lang="th">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #05060a; }} #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
      <div id="caps" data-composition-id="caps" data-composition-src="compositions/captions.html" data-start="0" data-duration="{DUR}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 100"></div>
      <!-- built by tools/scenekit.py from timeline.json (cue-based); sounds: freesound CC0, see assets/sources.txt; render: --resolution portrait-4k --fps 60 -->
{chr(10).join(auds)}
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
'''
    write(os.path.join(hf, "index.html"), idx)
    json.dump(resolved, open(os.path.join(hf, "timeline_resolved.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # duplicate id check across every composition
    for f in sorted(os.listdir(os.path.join(hf, "compositions"))):
        if f.endswith(".html"):
            ids = re.findall(r'\sid="([^"]+)"', open(os.path.join(hf, "compositions", f), encoding="utf-8").read())
            dup = sorted({i for i in ids if ids.count(i) > 1 and "${" not in i})
            if dup:
                print(f"DUPLICATE ids in {f}: {dup[:8]}")
    for s in resolved["scenes"]:
        print(f'{s["id"]} {s["module"]:<16} {s["start"]:>7.2f} - {s["end"]:>6.2f}  ({s["dur"]:.2f}s)  phrases {s["phrases_inside"]}')
    print(f"duration {DUR}s, {len(auds)} audio clips")
