# ตรวจ เรนเดอร์ และส่งงาน

## ตรวจ (ก่อนเรนเดอร์ทุกครั้ง)

```sh
python hf/build.py
npx hyperframes check --json > render/check.json
npx hyperframes snapshot --no-end --describe false -o <dir> --at <เวลาหลังจุดสำคัญของทุกฉาก>
```

| ที่ check แจ้ง | แก้ |
|---|---|
| `content_overlap` (error) | ย้ายข้อความ/การ์ด หรือใส่ `data-layout-ignore` ให้ตัวหนังสือที่เป็นลวดลายฉาก |
| `line_unread` | ให้ข้อความขึ้นเร็วขึ้น/ค้างนานขึ้น (0.5 วิ + 0.3 วิต่อคำ) หรือย่อข้อความ; บรรทัดสุดท้ายของคลิปต้องค้าง ≥ 2 วิ |
| `text_below_floor` | ตัวหนังสือ ≥ 28 px |
| `contrast_aa_failure` | พื้นหลังซับต้องเข้มพอ (หรือเปลี่ยนสีข้อความ) |
| `dead_stretch` | เพิ่มการขยับที่มีความหมาย |
| `gsap_timeline_set_initial_hide` | ซ่อนตั้งแต่ต้นด้วย fromTo ตัวแรก แทน `tl.set` ที่เวลา 0 |
| `duplicate_audio_track` | ไฟล์เดียวกันซ้อนบน track เดียว → ย้าย track |

ดูภาพนิ่ง: ตัวละครไม่ถูกการ์ด/ซับบังหน้า, ของในมืออยู่ตำแหน่งมือจริง, ของฉากหลังไม่ซ้อนของหน้าฉาก, แขนไม่พาดหน้า, ช่วงรอยต่อเห็นสองช็อตซ้อนกัน (cross-dissolve ทำงาน)

## เรนเดอร์และส่งงาน

```sh
npx hyperframes render --quality high --gpu --browser-gpu --workers 10 --resolution portrait-4k --fps 60 -o ../render/<slug>-epN_v1_4k60.mp4
ffmpeg -y -i render/<f>_4k60.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 320k render/<f>_4k60_lufs14.mp4
ffmpeg -y -i render/<f>_4k60_lufs14.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -preset medium -crf 22 -c:a aac -b:a 160k render/<f>_1080p_preview.mp4
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of compact render/<f>_4k60_lufs14.mp4
```

- `--quality high` = "High Quality" ใน Studio (CRF 15); `--gpu` = เข้ารหัสด้วย NVENC (ถ้าไม่มี NVIDIA ให้ตัดออก); เวลาส่วนใหญ่คือการจับภาพ Chrome (CPU)
- ความดังเป้า −14 LUFS: มิกซ์ที่มีช่วงเงียบเยอะมักออก −15 ถึง −17 → ปรับเฉพาะเสียงด้วย `-c:v copy` ไม่ต้องเรนเดอร์ภาพใหม่
- ไฟล์ 4K ใหญ่เกินส่งเข้ามือถือ → ส่งสำเนา 1080p คู่กันเสมอ
- ดึงภาพนิ่งจากไฟล์จริงเช็กอีกรอบก่อนรายงาน
