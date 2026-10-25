# สไตล์ภาพ flood (flatkit)

ลุค: flat vector ไม่มีเส้นขอบ, ตัวละครหน้าตรง หัวโตกึ่งชิบิ หน้าตาเหนื่อย/กังวล (เปลือกตาตก ถุงใต้ตา แก้มแดง), เงาไล่น้ำหนักนุ่ม, แสงเรือง + ลำแสง (screen blend), vignette หนัก, เกรนบาง ๆ, การ์ดความรู้สีครีมมีวงกลมแดงเลขข้อ, การ์ดตัวเลขนับขึ้นลงพร้อมแถบ, ป้าย EP มุมซ้ายบน, ซับขาวตัวหนาเน้นคำด้วยป้ายแดง, ฉากปิดเป็นการ์ดแบบปฏิทิน/ใบนัด

ใช้งาน: `series/<slug>/lib/hud.py` ตั้ง `KIT = "flat"` → `ctx.scene(...)` ห่อด้วย `tools/flatkit.py` และฝัง `tools/flatkit.js` ให้ทุกฉาก

## ในโค้ด JS ของฉากมีให้ใช้

| ชื่อ | ทำอะไร |
|---|---|
| `person(o)` | ตัวละครหน้าตรง คืน `{ svg, neck, sL, sR, hy, shY, ax, ay, armL, ... }` (จุดกำเนิด = พื้นระหว่างเท้า) |
| `armTo(r, sg, x, y, bend, glove)` | แขนงอ 2 ท่อนไปจับจุด (sg −1 ซ้ายจอ/1 ขวาจอ; `bend: -1` ให้ข้อศอกออกนอก ใช้ตอนชูมือ/โบก ไม่งั้นแขนพาดหน้า) ใส่ `extra: ["noArmL"/"noArmR"]` เพื่อซ่อนแขนเดิม |
| `cat(o)` | แมวนั่งหน้าตรง (`c`, `c2`, `eye`, `collar`, `plain`) |
| `place(svg, x, y, s, id)` | วางของ; กลุ่มด้านใน (`id`) คือตัวที่ animate |
| `glow(x, y, r, name, op)` | แสงเรือง: amber, warm, red, cold, green, pink, neon, eye, white |
| `cone(x, y, angle, len, spread, color, op)` | ลำแสง (0° = ขวา, 90° = ลง) |
| `led("02:13", h, color)` | ตัวเลข 7 ส่วนแบบนาฬิกา LED คืน `{ svg, w }` |
| `VIG`, `SH`, `SHV` | vignette / เงาไล่ด้านข้าง / เงาไล่บนลง (url ของ defs) |
| `ft(sel, from, to, t)` | fromTo ที่ข้ามเป้าหมายที่ไม่มี และไม่ render ซ้ำเมื่อ tween ตัวเดิมหลายครั้ง |
| `pop(sel, t, hold)` · `cardIn(sel, t, hold)` | ข้อความ/การ์ดเด้งเข้า (และออกหลัง hold) |
| `count(el, a, b, t, d, dec)` | ตัวเลขนับขึ้น/ลง |
| `face(id, "fP", t)` | เปลี่ยนหน้าแบบ crossfade: fN ปกติ · fS ตกใจ · fH ยิ้ม · fP ตาแดง/เขี้ยว · fQ สงสัย |
| `shot`, `alive`, `flicker` | หลักความลื่น (ดู smooth-motion.md) |

### ตัวเลือกของ `person()`

- `hair`: bob, pony, long, spiky, short, old, bun, chignon · `hairC`
- สี: `skin`, `skinD`, `brow`, `shirt`, `pants`, `shoe`, `sleeve`, `glove`, `lip` (ใส่แล้วเป็นปากเติมสี), `pattern` (ลายเสื้อ SVG) + `patW`
- รูปทรง: `coat` (+ `coatLong`), `skirt` (+ `skirtLong`, `legC`), `longSleeve`, `kid`, `hs` (ขนาดหัว), `sw` (ความกว้างไหล่), `armSpread`
- หน้า: `alert: true` (ตาตื่น ไม่มีเปลือกตาตก), `smile`, `lash`
- `extra`: mole, earrings, badge (`badgeC`), steth, beads, zip, vneck, collar, pocketpen, hood, pack, headband (`bandC`), nursecap, hairpin, glasses, mask (`maskC`), surgcap / cap (`capC`), strawhat, mustache, noArmL, noArmR

## ฉาก (series lib/sets.py)

- เป็นฟังก์ชัน JS ใน string `JS` คืน SVG; แบ่งชั้น `<g id="${P}-far|mid|near">` ให้ `shot()` เลื่อนต่างความเร็ว และมีพารามิเตอร์ `slot` (SVG ที่แทรกระหว่าง mid กับ near เช่นคนยืนหลังโต๊ะ)
- ไฟที่ไหวได้ใส่ id (`${P}-lamp`, `${P}-tube`, `${P}-neon`) แล้ว `flicker()` ในฉาก
- ตัวหนังสือในฉากเป็นลวดลาย: ใส่ `data-layout-ignore` และไม่ต่ำกว่า 28 px (ฟังก์ชัน `T()` ทำให้แล้ว)

## การ์ด/ป้าย (series lib/hud.py)

`ep_tag`, `card(n, icon, title, sub, tag)`, `stat(n, icon, label, value, unit)` (+ `#id-num`, `#id-bar`), `chip`, `bubble`, `receipt`, `appt` (การ์ดปิดตอน), `series_line`, `title` (ชื่อเรื่องใหญ่)

## ข้อควรระวังที่เจอจริง

- cross-dissolve ต้องให้ `#root` ของฉากโปร่งใส (flatkit ทำให้แล้ว) สีพื้นอยู่ที่ชั้นเฟด
- yoyo ที่ต้องจบที่ค่าปลายใช้ `repeat` เลขคู่ (นีออนกระพริบ repeat 3 จะดับค้าง)
- พื้นสว่างใต้แถบซับทำให้ซับขาวอ่านยาก → ทำพื้นช่วง y 1232–1400 ให้เข้ม; แสงแบนสว่างหลังซับก็เช่นกัน ใช้ radialGradient ที่จางก่อนถึงแถบ
- ภาพกล้องกลางคืนสีเขียว: ทับด้วย rect สีเขียว `style="mix-blend-mode: color"` แต่สีที่อยากให้เด่น (ตาแดง) วาด "หลัง" ชั้นสี
- ของประกอบฉากหลังที่ซ้อนกับของหน้าฉาก (ถังขยะหลังโต๊ะ) ให้ปิดด้วยพารามิเตอร์ของฉาก
- ไฟล์ 4K60 ใหญ่ (≈60 Mbps) เพราะเกรนบนภาพที่ซูมตลอด ลด `grain` ใน `ctx.scene(..., grain=0.04)` ถ้าต้องการไฟล์เล็ก
