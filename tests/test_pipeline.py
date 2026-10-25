"""Smoke tests: workspace → series → episode → build (flat kit), captions in the flood style, cue grammar, installer.

run: python -m unittest discover -s tests -v      (needs: soundfile)
"""
import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def run(*args, cwd=None, env=None):
    return subprocess.run([PY, *map(str, args)], cwd=cwd, env=env or ENV, capture_output=True, text=True, encoding="utf-8")


class Pipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.ws = Path(cls.tmp.name) / "ws"
        r = run(ROOT / "scripts" / "setup_workspace.py", "--root", cls.ws)
        assert r.returncode == 0, r.stderr
        r = run(cls.ws / "tools" / "new_series.py", "--root", cls.ws, "--slug", "demo", "--title", "ทดสอบ", "--episodes", "2")
        assert r.returncode == 0, r.stderr
        r = run(cls.ws / "tools" / "new_episode.py", "--root", cls.ws, "--series", "demo", "--ep", "1", "--title", "ตอนทดลอง", "--date", "2026-01-01", "--no-fonts")
        assert r.returncode == 0, r.stderr
        cls.ep = cls.ws / "projects" / "2026-01-01_demo-ep1"
        timings = {"duration": 3.0, "phrases": [{"text": "ทดสอบหนึ่งสองสาม", "section": "hook", "start": 0.2, "end": 2.6}]}
        (cls.ep / "voiceover" / "timings_final.json").write_text(json.dumps(timings, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_workspace_layout(self):
        for p in ["tools/scenekit.py", "tools/flatkit.js", "templates/series-flood/lib/looks.py", "logs/lessons.md", "assets/licences.md",
                  "series/demo/series.json", "series/demo/lib/hud.py"]:
            self.assertTrue((self.ws / p).exists(), p)
        self.assertEqual(json.loads((self.ws / "series/demo/series.json").read_text(encoding="utf-8"))["title"], "ทดสอบ")

    def test_build_flat_episode(self):
        r = run(self.ep / "hf" / "build.py")
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        comp = (self.ep / "hf" / "compositions" / "s01-hook.html").read_text(encoding="utf-8")
        self.assertIn("function FLATKIT", comp)
        self.assertIn('window.__timelines["s01"]', comp)
        caps = (self.ep / "hf" / "compositions" / "captions.html").read_text(encoding="utf-8")
        self.assertIn("Prompt", caps)
        idx = (self.ep / "hf" / "index.html").read_text(encoding="utf-8")
        self.assertIn('data-composition-id="g01"', idx)
        resolved = json.loads((self.ep / "hf" / "timeline_resolved.json").read_text(encoding="utf-8"))
        self.assertAlmostEqual(resolved["duration"], 5.4, places=2)

    def test_cue_grammar(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import scenekit
        tl = scenekit.Timeline(str(self.ep / "hf"))
        self.assertAlmostEqual(tl.resolve("p0"), 0.2)
        self.assertAlmostEqual(tl.resolve("p0.end+0.4"), 3.0)
        self.assertAlmostEqual(tl.resolve("end-0.4"), 5.0)
        with self.assertRaises(ValueError):
            tl.resolve("nope")


class Captions(unittest.TestCase):
    def test_flood_pills(self):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d) / "t.json"
            t.write_text(json.dumps({"phrases": [{"text": "ขยะติดเชื้อทุกถุง", "start": 0.3, "end": 1.5}]}, ensure_ascii=False), encoding="utf-8")
            out = Path(d) / "c.html"
            r = run(ROOT / "scripts" / "build_captions.py", t, out, "--style", "flood", "--hl", "ติดเชื้อ=#e5483a")
            self.assertEqual(r.returncode, 0, r.stderr)
            html = out.read_text(encoding="utf-8")
            self.assertIn('class="hl" style="background:#e5483a"', html)
            self.assertIn("Prompt", html)


class Installer(unittest.TestCase):
    def test_dry_run_and_install(self):
        with tempfile.TemporaryDirectory() as d:
            env = {**ENV, "HOME": d, "USERPROFILE": d}
            r = run(ROOT / "install.py", "--agent", "both", "--dry-run", env=env)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("would install", r.stdout)
            self.assertFalse((Path(d) / ".claude").exists())
            r = run(ROOT / "install.py", "--agent", "claude", env=env)
            self.assertIn("installed", r.stdout)
            self.assertTrue((Path(d) / ".claude/skills/storytelling-motion/SKILL.md").exists())
            r = run(ROOT / "install.py", "--agent", "claude", env=env)
            self.assertIn("up to date", r.stdout)
            (Path(d) / ".claude/skills/storytelling-motion/SKILL.md").write_text("edited", encoding="utf-8")
            r = run(ROOT / "install.py", "--agent", "claude", env=env)
            self.assertIn("skipped", r.stdout)


if __name__ == "__main__":
    unittest.main()
