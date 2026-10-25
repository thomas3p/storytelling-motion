"""Build ปอบยุค 5G ตอนที่ 1 from timeline.json + scenes/*.py (modular, cue-based, flood look via tools/flatkit; see tools/scenekit.py)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
# the pipeline lives in <workspace>/tools (installed workspace) or <repo>/scripts (this repository)
for d in ("tools", "scripts"):
    sys.path.insert(0, os.path.join(HERE, "..", "..", "..", d))
from scenekit import build_episode

build_episode(HERE, "ปอบยุค 5G ตอนที่ 1")
