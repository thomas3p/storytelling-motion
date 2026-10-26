# โครงสร้างแบบโมดูล (scenekit)

ฉากละไฟล์ + ไทม์ไลน์อิงจุดเสียง เพื่อให้เปลี่ยน/อัดเสียงใหม่แล้วทุกอย่างตามได้เอง และให้เอเจนต์หลายตัวทำฉากพร้อมกันได้ (แจกฉากละไฟล์ ห้ามแตะ timeline.json, lib และไฟล์ฉากของคนอื่น)

## ไฟล์ของตอน

```
projects/<date>_<slug>-epN/
  voiceover/  vo_text.txt · style.txt · captions.txt · timings_final.json (จาก voiceover.md)
  hf/         build.py · timeline.json · scenes/sNN_*.py · scenes/g_ep.py · assets/{audio/vo.wav, sfx/, bgm/, fonts/}
```

`python hf/build.py` เขียน `compositions/*.html`, `compositions/captions.html`, `index.html`, `timeline_resolved.json` และตรวจ id ซ้ำ

## timeline.json

```json
{
  "series_lib": "../../../series/<slug>/lib",
  "duration": "p16.end+2.8",
  "xfade": 0.3,
  "cues": { "title": "p1+1.5", "fact": "p7+4.56" },
  "scenes": [ { "id": "s01", "module": "s01_hook", "start": "0" }, { "id": "s02", "module": "s02_city", "start": "p1-0.3" } ],
  "globals": [ { "id": "g01", "module": "g_ep", "start": "p2-0.3", "end": "p16.end" } ],
  "audio": [ { "id": "vo", "src": "audio/vo.wav", "at": "0", "dur": "file", "track": 10 },
             { "id": "sfx-door", "src": "sfx/door.mp3", "at": "p5.end+0.1", "dur": 1.2, "vol": 0.6, "fi": 0, "fo": 0.2, "ms": 0, "track": 15 } ],
  "captions": { "style": "flood", "top": 1232, "size": 54, "skip": [14], "last_until": "p16.end+0.1",
                "hl": { "คำสำคัญ": "#e5483a" }, "overrides": { "8": { "shift": 0.1, "hold": 0.4, "text": "ข้อความแสดง", "hide": false } } }
}
```

- **จุดเสียง (cue)**: `p7` (ต้นวลี 7), `p7.end`, `s03` (ต้นฉาก), ชื่อ cue, `end` (จบคลิป), ตัวเลขวินาที ± ส่วนต่าง เช่น `p7.end+0.25` ห้ามพิมพ์วินาทีตายตัวในฉาก
- ฉากเริ่ม ~0.3 วิก่อนวลีแรกของฉาก (`"p5-0.3"`) และ cue ในวลีหาได้จากเวลาคำ (`tools/seg_words.py`)
- `xfade`: ฉากเล่นต่อใต้ฉากถัดไปอีก xfade วินาที แล้วฉากใหม่เฟดทับ (สลับ track, z-index เพิ่มขึ้น)
- `globals`: ของที่คร่อมหลายฉาก เช่นป้าย EP มุมซ้ายบน
- `audio`: `dur` เป็นวินาที, cue ปลายทาง, หรือ `"file"` (ความยาวไฟล์); `ms` = เริ่มกลางไฟล์; ไฟล์เดียวกันห้ามซ้อนบน track เดียวกัน; เสียงยาวกว่าไฟล์ต้องแบ่งหลายท่อน
- `captions`: `style: "flood"` = ตัวหนาขาว เงานุ่ม คำสำคัญเป็นป้ายสี (`hl` คำ → สีพื้นป้าย); `skip` วลีที่ฉากแสดงเป็นตัวหนังสือเอง (เช่นกล่องคำพูด); ข้อความแสดงผลต่างจากคำอ่านได้ด้วย `คำอ่าน || ข้อความแสดง` ใน captions.txt และขึ้นบรรทัดใหม่ตรงที่ต้องการด้วย `|` ในข้อความแสดง (เบราว์เซอร์ตัดบรรทัดภาษาไทยกลางคำได้ เช่น "ก็ | คือ")

## ไฟล์ฉาก

```python
"""s03 setup: one line saying what the scene shows."""
SCENE = {"title": "lobby"}

def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, tq = ctx.dur, ctx.t("queue")               # ctx.t(cue) = เวลาในฉาก
    overlays = H.chip("s03-c", 1, "ข้อความ", 70, 250)
    js = L.JS + S.JS + f"""
    const pim = person({{ ...PIM, id: "s03-pim" }});
    $("s03-v").innerHTML = lobby() + place(pim.svg, 540, 1190, 1.0, "s03-pimg") + VIG;
    shot({d:.2f}, 1.07, 0, -20, [["#s03-far", 10], ["#s03-near", -16]]);
    alive("s03-pim", pim, "s03-pimg", 0, {d:.2f});
    pop("#s03-c", {tq:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#d7bfbd")
```

- id ทุกตัวขึ้นต้นด้วย id ฉาก (`s03-…`) กันชนกัน
- ตัวละครวางเท้าที่ y ≈ 1190 (แถบซับอยู่ y 1232–1400) การ์ดอยู่ y 230–450 ป้าย EP y 176
- ของที่ใช้ร่วมกันหลายฉากในตอนเดียว: `hf/scenes/_shared.py`

## คำสั่ง

```sh
python hf/build.py
npx hyperframes check --json            # แก้ทุก error, ชั่งทุก warning
npx hyperframes snapshot --no-end --describe false -o <dir> --at 2.0,7.2,10.6
npx hyperframes render --quality high --gpu --browser-gpu --workers 10 --resolution portrait-4k --fps 60 -o ../render/<slug>-epN_v1_4k60.mp4
```
