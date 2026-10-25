#!/usr/bin/env python3
"""Install the storytelling-motion skill for Claude Code and/or Codex, and optionally create a workspace.

usage:
  python install.py --agent claude                      (~/.claude/skills/storytelling-motion)
  python install.py --agent codex                       (~/.agents/skills/storytelling-motion)
  python install.py --agent both --project "<folder>"   (<folder>/.claude/skills/… and <folder>/.agents/skills/…)
  python install.py --agent claude --workspace "<folder>"   (also create tools/, series/, projects/, logs/ there)
  options: --replace (back up a different existing copy, then install) · --dry-run (print the plan, change nothing)

Only the skill files are copied (SKILL.md, references/, scripts/, templates/). Nothing is downloaded, no API key is read,
and an existing skill that differs is never overwritten without --replace (the old copy goes to skill-backups/).
"""
from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

SKILL_NAME = "storytelling-motion"
HERE = Path(__file__).resolve().parent
PAYLOAD = ["SKILL.md", "references", "scripts", "templates"]
SKIP = {"__pycache__", ".git"}


def payload_files(root: Path) -> list[Path]:
    out = []
    for item in PAYLOAD:
        p = root / item
        if p.is_file():
            out.append(Path(item))
        elif p.is_dir():
            for base, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP]
                for f in files:
                    if not f.endswith((".pyc", ".pyo")):
                        out.append(Path(base, f).relative_to(root))
    return sorted(out)


def same_install(dst: Path) -> bool:
    if not dst.exists():
        return False
    mine = payload_files(HERE)
    if sorted(payload_files(dst)) != mine:
        return False
    return all(filecmp.cmp(HERE / f, dst / f, shallow=False) for f in mine)


def install_to(dst: Path, replace: bool, dry: bool) -> str:
    if same_install(dst):
        return f"up to date: {dst}"
    if dst.exists():
        if not replace:
            return (f"skipped: {dst} already has a different copy (your edits?). "
                    f"Re-run with --replace to back it up to {dst.parent.parent / 'skill-backups'} and install this version.")
        backup = dst.parent.parent / "skill-backups" / f"{SKILL_NAME}-{datetime.now():%Y%m%d-%H%M%S}"
        if dry:
            return f"would back up {dst} → {backup} and install"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(dst), str(backup))
    if dry:
        return f"would install {len(payload_files(HERE))} files → {dst}"
    for rel in payload_files(HERE):
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(HERE / rel, out)
    return f"installed: {dst}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--agent", choices=["claude", "codex", "both"], default="claude")
    ap.add_argument("--project", help="install into this project instead of your user folder")
    ap.add_argument("--workspace", help="also create a storytelling workspace here")
    ap.add_argument("--replace", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if sys.version_info < (3, 10):
        print("Python 3.10 or newer is required."); return 1
    base = Path(a.project).resolve() if a.project else Path.home()
    targets = {"claude": [".claude"], "codex": [".agents"], "both": [".claude", ".agents"]}[a.agent]
    for t in targets:
        print(install_to(base / t / "skills" / SKILL_NAME, a.replace, a.dry_run))
    if a.workspace:
        if a.dry_run:
            print(f"would create workspace: {Path(a.workspace).resolve()}")
        else:
            sys.path.insert(0, str(HERE / "scripts"))
            import setup_workspace
            setup_workspace.setup(a.workspace)
    return 0


if __name__ == "__main__":
    sys.exit(main())
