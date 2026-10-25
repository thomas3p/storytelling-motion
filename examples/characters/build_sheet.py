"""Write characters.html: a character sheet of the example cast (templates/series-flood/lib/looks.py) drawn with scripts/flatkit.js.
Open the HTML in any browser — no HyperFrames needed. Re-run after editing a look:  python examples/characters/build_sheet.py
Optional PNG:  python examples/characters/build_sheet.py --png   (uses a local Chrome/Edge in headless mode)
"""
import argparse, importlib.util, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))


def load(path):
    spec = importlib.util.spec_from_file_location("m", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


# (look, id, label, role, face, x, feet y, scale) — row 1 the main cast, row 2 variants, faces and side characters
CAST = [
    ("PIM", "c1", "หมอพิม", "ศัลยแพทย์สายเลือดปอบ", "fN", 330, 1040, 1.15),
    ("FON", "c2", "ฝน", "พยาบาลผู้ช่วยคนใหม่", "fN", 830, 1040, 1.15),
    ("TEY", "c3", "อาจารย์เต้ย", "หมอผียุคใหม่", "fN", 1330, 1040, 1.15),
    ("GRANNY", "c4", "ยายปอบ", "ปอบสมัยก่อน", "fP", 1830, 1040, 1.1),
    ("PIM", "c5", "หมอพิม · หิว", "หน้า fP", "fP", 200, 1880, 0.8),
    ("PIM_OR", "c6", "หมอพิม · ห้องผ่าตัด", "PIM_OR", "fN", 470, 1880, 0.8),
    ("PIM_SIL", "c7", "เงาในกล้อง", "PIM_SIL", "fP", 740, 1880, 0.8),
    ("FON", "c8", "ฝน · ตกใจ", "หน้า fS", "fS", 1010, 1880, 0.8),
    ("FON", "c9", "ฝน · สงสัย", "หน้า fQ", "fQ", 1280, 1880, 0.8),
    ("CLIENT_A", "c10", "ลูกค้า A", "CLIENT_A", "fN", 1550, 1880, 0.8),
    ("DRIVER", "c11", "คนขับรถขยะ", "DRIVER", "fQ", 1820, 1880, 0.8),
]


def build(png=False):
    looks = load(os.path.join(ROOT, "templates", "series-flood", "lib", "looks.py"))
    kit = open(os.path.join(ROOT, "scripts", "flatkit.js"), encoding="utf-8").read()
    figs = []
    for look, cid, label, role, face, x, y, s in CAST:
        figs.append(f'{{ look: {look}, id: "{cid}", label: "{label}", role: "{role}", face: "{face}", x: {x}, y: {y}, s: {s} }}')
    cast_js = (",\n" + " " * 2).join(figs)
    html = f"""<!doctype html>
<html lang="th"><head><meta charset="utf-8" /><title>Example cast · flatkit</title>
<link rel="preconnect" href="https://fonts.googleapis.com" /><link href="https://fonts.googleapis.com/css2?family=Prompt:wght@500;700&family=Mitr:wght@600&display=swap" rel="stylesheet" />
<style>html, body {{ margin: 0; background: #0b0f1e; }} svg {{ display: block; width: 100%; height: auto; font-family: "Prompt", sans-serif; }}</style></head>
<body>
<svg width="0" height="0" style="position: absolute"><defs id="cs-defs"></defs></svg>
<svg id="sheet" viewBox="0 0 2160 2160" xmlns="http://www.w3.org/2000/svg"></svg>
<script>
{kit}
const K = FLATKIT("cs", null);
const {{ person, cat, place, glow, f1 }} = K;
{looks.JS}
const CAST = [
  {cast_js}
];
let s = `<rect width="2160" height="2160" fill="#0b0f1e" /><rect width="2160" height="2160" fill="url(#cs-vig)" />`;
s += `<text x="1080" y="110" text-anchor="middle" font-size="64" font-weight="700" fill="#ffffff">ปอบยุค 5G · ชุดตัวละครตัวอย่าง</text>`;
s += `<text x="1080" y="170" text-anchor="middle" font-size="34" font-weight="500" fill="#9aa6c0">flatkit.js · สไตล์ flood — ตัวละครหน้าตรง หัวโต แสงเงานุ่ม · ใช้เป็นแบบได้ (MIT)</text>`;
s += `<rect x="60" y="1235" width="2040" height="4" rx="2" fill="#1c2640" />`;
for (const c of CAST) {{
  const r = person({{ ...c.look, id: c.id }});
  s += glow(c.x, c.y - 330 * c.s, 300 * c.s, "warm", 0.12);
  s += `<ellipse cx="${{c.x}}" cy="${{c.y + 6}}" rx="${{110 * c.s}}" ry="${{16 * c.s}}" fill="#000" opacity="0.35" />`;
  s += place(r.svg, c.x, c.y, c.s);
  s += `<text x="${{c.x}}" y="${{c.y + 70 * Math.max(c.s, 0.9)}}" text-anchor="middle" font-size="${{c.s > 1 ? 44 : 30}}" font-weight="700" fill="#fbf3dc">${{c.label}}</text>`;
  s += `<text x="${{c.x}}" y="${{c.y + 70 * Math.max(c.s, 0.9) + (c.s > 1 ? 44 : 34)}}" text-anchor="middle" font-size="${{c.s > 1 ? 30 : 24}}" font-weight="500" fill="#9aa6c0">${{c.role}}</text>`;
}}
// the clinic's black cat
s += place(cat({{ ...LIPO, id: "c12" }}), 2030, 1880, 0.9);
s += `<text x="2030" y="1950" text-anchor="middle" font-size="30" font-weight="700" fill="#fbf3dc">ไลโป</text><text x="2030" y="1984" text-anchor="middle" font-size="24" font-weight="500" fill="#9aa6c0">แมวดำ · cat()</text>`;
s += `<text x="1080" y="2110" text-anchor="middle" font-size="28" font-weight="500" fill="#5a6684">templates/series-flood/lib/looks.py · หน้า fN ปกติ · fS ตกใจ · fH ยิ้ม · fP ตาแดง/เขี้ยว · fQ สงสัย</text>`;
document.getElementById("sheet").innerHTML = s;
// pick each figure's face
for (const c of CAST) for (const f of ["fN", "fS", "fH", "fP", "fQ"]) {{ const el = document.getElementById(`${{c.id}}-${{f}}`); if (el) el.setAttribute("opacity", f === c.face ? 1 : 0); }}
</script>
</body></html>
"""
    out = os.path.join(HERE, "characters.html")
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out)
    if png:
        exe = next((p for p in [shutil.which("chrome"), shutil.which("google-chrome"), shutil.which("msedge"),
                                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"] if p and os.path.exists(p)), None)
        if not exe:
            sys.exit("no Chrome/Edge found for --png")
        png_path = os.path.join(HERE, "characters.png")
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=2160,2160", "--virtual-time-budget=8000",
                        f"--screenshot={png_path}", "file:///" + out.replace("\\", "/")], check=True)
        print("wrote", png_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--png", action="store_true")
    build(ap.parse_args().png)
