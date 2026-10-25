"""Start a new series from the flood template (the example cast of ปอบยุค 5G).

usage: python tools/new_series.py --root <workspace> --slug myseries --title "ชื่อซีรีส์" [--episodes 8]
Copies templates/series-flood → series/<slug> (lib/looks.py, sets.py, hud.py + series.json with your title/slug).
Then edit lib/looks.py (characters) and lib/sets.py (places); the template's cast and sets stay as working examples.
"""
import argparse, json, os, shutil


def main(a):
    root = os.path.abspath(a.root)
    src = os.path.join(root, "templates", "series-flood")
    dst = os.path.join(root, "series", a.slug)
    if os.path.exists(dst):
        raise SystemExit(f"{dst} already exists — not overwriting")
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
    p = os.path.join(dst, "series.json")
    cfg = json.load(open(p, encoding="utf-8"))
    cfg.update({"title": a.title, "slug": a.slug, "episodes_planned": a.episodes})
    json.dump(cfg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"series ready: {dst}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True); ap.add_argument("--slug", required=True); ap.add_argument("--title", required=True)
    ap.add_argument("--episodes", type=int, default=8)
    main(ap.parse_args())
