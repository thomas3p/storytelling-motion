# เสียงพากย์ (Gemini TTS API) และการจับเวลา

## เจนเสียง

- ผู้ใช้สร้าง API key เองใน Google AI Studio แล้วตั้งเป็นตัวแปร `GEMINI_API_KEY` ในเครื่อง (เช่น Windows: System Properties → Environment Variables) เอเจนต์ห้ามขอ/พิมพ์/บันทึกค่าคีย์
- **เจนทั้งบทในครั้งเดียว** เสียงจะต่อเนื่องเป็นคนเดียวกันทั้งคลิป
- **ล็อกน้ำเสียงทั้งซีรีส์ด้วย seed**: model, voice, seed, temperature (1.0), API และ `style_base` เดิมทุกตอน (เก็บใน series.json) อารมณ์แต่ละเทคต่างกันได้ ซึ่งปกติ
- **เพศของเสียงต้องตรงกับ style** ไม่งั้นเพศจะสลับไปมาระหว่างเทค (`GET /v1beta/voices` บอก gender/pitch/persona ของแต่ละเสียง) ตัวอย่างผู้บรรยายชาย: `en-us-storyteller-14`
- `vo_text.txt` บรรทัดละวลี ตัวเลขเขียนเป็นคำอ่าน ใช้ `…` ตรงที่อยากให้เว้นจังหวะ; `style.txt` บอกอารมณ์ทีละช่วง (ไม่ใส่ในตัวบท ไม่งั้นจะถูกอ่านออกเสียง)

```sh
python tools/aistudio_tts.py --series series/<slug>/series.json --text voiceover/vo_text.txt --style voiceover/style.txt --out voiceover/vo_full.wav
```

## ตัด/ปรับ/จับเวลา

```sh
python tools/tighten_vo.py voiceover/vo_full.wav voiceover/vo_tight.wav --keep 0.35
ffmpeg -y -i voiceover/vo_tight.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 voiceover/vo.wav
python tools/seg_words.py voiceover/vo.wav 0 <ความยาว>          # ถอดเสียงพร้อมเวลาคำ
python tools/align_asr.py voiceover/vo.wav voiceover/captions.txt voiceover/timings_asr.json
python tools/snap_timings.py voiceover/vo.wav voiceover/timings_asr.json voiceover/timings.json
python tools/insert_gaps.py voiceover/vo.wav voiceover/timings.json voiceover/vo_final.wav voiceover/timings_final.json 1:0.5 8:0.6
cp voiceover/vo_final.wav hf/assets/audio/vo.wav
```

- **เทียบข้อความที่ถอดได้กับบททุกบรรทัด**: โมเดลอาจพูดเกิน (แทรกประโยค) หรือข้ามคำ → ประโยคเกินให้ตัดออกจากเทคเดิมตรงช่วงเงียบ, คำที่หายให้แก้ซับตามเสียงจริงแล้วปรับภาพให้ตรง
- align มักหลุดท่อนท้าย (m=0.00) → ใช้เวลาคำจาก seg_words + ช่วงเงียบ (`ffmpeg -af silencedetect=n=-40dB:d=0.12`) แก้ timings.json ด้วยมือ
- `insert_gaps` เว้นจังหวะหลังวลีสำคัญ (การ์ดชื่อเรื่อง, หักมุม, ประโยคปิด) ครั้งละ 0.3–0.6 วิ
- เช็กเพศเสียงด้วยระดับเสียงกลาง (librosa pyin): ผู้ชายราว 85–105 Hz
