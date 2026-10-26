"""Build 60°C รุ่งอรุณเดือด ตอนที่ 1 from timeline.json + scenes/*.py (modular, cue-based; see tools/scenekit.py)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ("tools", "scripts"):
    sys.path.insert(0, os.path.join(HERE, "..", "..", "..", d))
from scenekit import build_episode

build_episode(HERE, "60°C รุ่งอรุณเดือด ตอนที่ 1")
