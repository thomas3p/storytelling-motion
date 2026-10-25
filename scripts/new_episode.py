"""Scaffold an episode: projects/<date>_<slug>-epN/{brief.md, voiceover/, render/, hf/} with build.py, a timeline.json skeleton,
the EP tag (scenes/g_ep.py), a first example scene, HyperFrames project files and the OFL fonts.

usage: python tools/new_episode.py --root <workspace> --series <slug> --ep 1 --title "ชื่อตอน" [--date 2026-10-25] [--no-fonts]
Nothing existing is overwritten.
"""
import argparse, datetime, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))

BUILD = '''"""Build {series_title} ตอนที่ {ep} from timeline.json + scenes/*.py (modular, cue-based; see tools/scenekit.py)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ("tools", "scripts"):
    sys.path.insert(0, os.path.join(HERE, "..", "..", "..", d))
from scenekit import build_episode

build_episode(HERE, "{series_title} ตอนที่ {ep}")
'''

G_EP = '''"""Global EP tag (top-left) from the intro to the end card."""
SCENE = {{"title": "ep tag"}}


def build(ctx):
    H = ctx.lib.hud
    js = f"""
    pop("#{{ctx.sid}}-ep", 0.05);
    tl.to("#{{ctx.sid}}-ep", {{{{ opacity: 0, duration: 0.25, ease: "sine.in" }}}}, {{ctx.dur - 0.3:.2f}});"""
    return ctx.scene("", "", H.ep_tag(f"{{ctx.sid}}-ep", {ep}, "{title}"), js, bg="transparent", grain=0)
'''

S01 = '''"""s01 hook: replace with your opening shot (this example: the clinic lobby with the doctor, from the template cast)."""
SCENE = {"title": "hook"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d = ctx.dur
    js = L.JS + S.JS + f"""
    const pim = person({{ ...PIM, id: "s01-pim" }});
    $("s01-v").innerHTML = lobby() + place(pim.svg, 540, 1190, 1.0, "s01-pimg") + VIG;
    shot({d:.2f}, 1.07, 0, -20, [["#s01-far", 10], ["#s01-mid", -8]]);
    alive("s01-pim", pim, "s01-pimg", 0, {d:.2f});
    flicker("#s01-l2", 0, {d:.2f}, 0.8, 1, 0.4);"""
    return ctx.scene("", "", "", js, bg="#d7bfbd")
'''


def write_new(path, text):
    if os.path.exists(path):
        print("kept", os.path.relpath(path)); return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main(a):
    root = os.path.abspath(a.root)
    series_dir = os.path.join(root, "series", a.series)
    cfg = json.load(open(os.path.join(series_dir, "series.json"), encoding="utf-8"))
    date = a.date or datetime.date.today().isoformat()
    ep_dir = os.path.join(root, "projects", f"{date}_{a.series}-ep{a.ep}")
    hf = os.path.join(ep_dir, "hf")
    for d in ("voiceover", "render", "hf/scenes", "hf/compositions", "hf/assets/audio", "hf/assets/sfx", "hf/assets/bgm", "hf/assets/fonts"):
        os.makedirs(os.path.join(ep_dir, d), exist_ok=True)
    for f in ("hyperframes.json", "package.json"):
        src = os.path.join(root, "templates", "episode", "hf", f)
        if os.path.exists(src) and not os.path.exists(os.path.join(hf, f)):
            shutil.copy2(src, os.path.join(hf, f))
    write_new(os.path.join(hf, "build.py"), BUILD.format(series_title=cfg.get("title", a.series), ep=a.ep))
    write_new(os.path.join(hf, "scenes", "g_ep.py"), G_EP.format(ep=a.ep, title=a.title))
    write_new(os.path.join(hf, "scenes", "s01_hook.py"), S01)
    timeline = {
        "series_lib": f"../../../series/{a.series}/lib", "duration": "p0.end+2.8", "xfade": 0.3, "cues": {},
        "scenes": [{"id": "s01", "module": "s01_hook", "start": "0"}],
        "globals": [{"id": "g01", "module": "g_ep", "start": "0", "end": "p0.end"}],
        "audio": [{"id": "vo", "src": "audio/vo.wav", "at": "0", "dur": "file", "track": 10}],
        "captions": {"style": "flood", "top": 1232, "size": 54, "skip": [], "last_until": "p0.end+0.1", "hl": {}, "overrides": {}},
    }
    write_new(os.path.join(hf, "timeline.json"), json.dumps(timeline, ensure_ascii=False, indent=2) + "\n")
    write_new(os.path.join(ep_dir, "brief.md"), f"# บรีฟ: {cfg.get('title', a.series)} ตอนที่ {a.ep} · {a.title}\n\n**Logline:**\n\n## โครงเรื่อง\n1. Hook:\n2. Setup:\n3. Rising:\n4. Climax:\n5. Cliffhanger:\n\n## ส่วนจริง / ส่วนแต่ง\n- จริง:\n- แต่ง:\n\n## ค่าที่สมมติ\n-\n")
    if not a.no_fonts:
        sys.path.insert(0, HERE)
        import get_fonts
        try:
            get_fonts.main(os.path.join(hf, "assets", "fonts"))
        except Exception as e:  # offline: the episode still builds; fonts fall back until downloaded
            print("fonts not downloaded:", e)
    print(f"episode ready: {ep_dir}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True); ap.add_argument("--series", required=True); ap.add_argument("--ep", type=int, required=True)
    ap.add_argument("--title", default=""); ap.add_argument("--date"); ap.add_argument("--no-fonts", action="store_true")
    main(ap.parse_args())
