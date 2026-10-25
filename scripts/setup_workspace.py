"""Create (or top up) a storytelling workspace: tools/, templates/, series/, projects/, logs/, assets/licences.md.

usage: python setup_workspace.py --root <workspace> [--force-tools]
- tools/ gets a copy of this skill's scripts (the pipeline); existing tools are kept unless --force-tools.
- templates/ gets series-flood (the example cast) and episode; logs and licences are created only when missing.
Never touches existing series, projects or logs.
"""
import argparse, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)

LESSONS = "# บทเรียน\n\nจดสิ่งที่เจอระหว่างทำแต่ละตอน (ปัญหา → วิธีแก้) อ่านไฟล์นี้ก่อนเริ่มเรื่องใหม่ทุกครั้ง\n"
CONCEPTS = "# บันทึกคอนเซปต์\n\n| วันที่ | เรื่อง/ตอน | สถานะ/ไฟล์ | สรุปเรื่อง |\n|---|---|---|---|\n"
LICENCES = "# ที่มาของสื่อ (เสียงพากย์ / เสียงประกอบ / ดนตรี / ฟอนต์)\n\nรูปแบบ: `- วันที่ · ตอน · ไฟล์ — ลิงก์ (สัญญาอนุญาต) ชื่อเดิม · ใช้ทำอะไร`\n"


def copytree_missing(src, dst, force=False):
    for base, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        rel = os.path.relpath(base, src)
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in files:
            if f.endswith((".pyc",)):
                continue
            out = os.path.join(dst, rel, f)
            if force or not os.path.exists(out):
                shutil.copy2(os.path.join(base, f), out)


def write_missing(path, text):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)


def setup(root, force_tools=False):
    root = os.path.abspath(root)
    for d in ("series", "projects", "logs", "assets"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    copytree_missing(HERE, os.path.join(root, "tools"), force_tools)
    copytree_missing(os.path.join(SKILL, "templates"), os.path.join(root, "templates"))
    write_missing(os.path.join(root, "logs", "lessons.md"), LESSONS)
    write_missing(os.path.join(root, "logs", "concepts-log.md"), CONCEPTS)
    write_missing(os.path.join(root, "assets", "licences.md"), LICENCES)
    print(f"workspace ready: {root}")
    return root


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--force-tools", action="store_true", help="overwrite tools/ with this version of the scripts")
    a = ap.parse_args()
    setup(a.root, a.force_tools)
