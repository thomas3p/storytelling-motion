# Workspace (cloud session 2026-10-26)

งานที่ทำด้วย skill นี้ในเครื่อง cloud: ซีรีส์ **60°C รุ่งอรุณเดือด** (`series/glass-oven`) ตอนที่ 1 (`projects/2026-10-26_glass-oven-ep1`)

ไฟล์สื่อ (เสียง ฟอนต์ วิดีโอ) และสำเนา `tools/` `templates/` ไม่ได้เก็บใน git สร้างใหม่ได้จาก repo นี้:

```sh
python scripts/setup_workspace.py --root workspace                 # tools/ + templates/
cd workspace
python tools/get_fonts.py projects/2026-10-26_glass-oven-ep1/hf/assets/fonts
python series/glass-oven/sound/make_sounds.py projects/2026-10-26_glass-oven-ep1/hf/assets     # เสียงประกอบ/ดนตรีสังเคราะห์
# เสียงพากย์: วางไฟล์จริงที่ projects/…/voiceover/vo_full.wav แล้ว
python series/glass-oven/sound/align_silence.py projects/…/voiceover/vo_full.wav projects/…/voiceover/captions.txt projects/…/voiceover/timings_final.json
python projects/…/voiceover/word_cues.py projects/…/voiceover/timings_final.json   # → cues ใน hf/timeline.json
python series/glass-oven/sound/vo_intercom.py projects/…/voiceover/vo_full.wav projects/…/voiceover/timings_final.json projects/…/hf/assets/audio/vo.wav 17
python projects/2026-10-26_glass-oven-ep1/hf/build.py
cd projects/2026-10-26_glass-oven-ep1/hf && npx hyperframes@0.8.186 render --quality high --fps 60 --resolution portrait -o ../render/glass-oven-ep1_v2_1080p60.mp4
```

สถานะ EP1: ภาพ เสียงประกอบ และซับเสร็จ (v1) จับเวลาด้วยเสียงชั่วคราว MMS-tha (CC-BY-NC ห้ามเผยแพร่) รอไฟล์เสียง Nadine จาก Higgsfield
