"""Estimate named cues ("p7+1.23") from phrase timings by the keyword's character position inside its phrase.
usage: python voiceover/word_cues.py voiceover/timings_final.json  → paste the printed object into hf/timeline.json "cues" (keep "title").
WANT = cue name → (phrase index, keyword in the spoken text). After a new voiceover: align it, run this, rebuild."""
import json, sys
P = json.load(open(sys.argv[1], encoding="utf-8"))["phrases"]
WANT = {"t35": (0, "สามสิบห้า"), "t60": (0, "หกสิบ"), "f40": (2, "ชั้นสี่สิบ"), "glass": (2, "คอนโด"), "ozone": (4, "ชั้นโอโซน"), "rip": (4, "ฉีกขาด"),
        "glare": (5, "แสงแรก"), "burn": (5, "ร้อนจน"), "full": (6, "แอร์ทุก"), "boom": (7, "ระเบิด"), "boom2": (7, "ทีละเครื่อง"),
        "car": (9, "รถที่จอด"), "two": (9, "เกือบสององศา"), "five": (9, "ทุกห้านาที"), "half": (10, "ครึ่งชั่วโมงแรก"), "oven": (11, "ก็คือรถ"),
        "tap": (12, "น้ำจากก๊อก"), "boil": (12, "เดือดปุด"), "birds": (13, "ฝูงนก"), "lift": (14, "ลิฟต์ค้าง"), "stairs": (14, "เหลือแค่"), "forty": (14, "สี่สิบชั้น"),
        "cook": (15, "ก่อนร่างกาย"), "icom": (16, "อินเตอร์คอม"), "ring": (16, "ดังขึ้น")}
out = {}
for k, (i, w) in WANT.items():
    t = P[i]["text"]; pos = t.find(w); assert pos >= 0, (k, w)
    off = (P[i]["end"] - P[i]["start"]) * pos / len(t)
    out[k] = f"p{i}+{off:.2f}"
print(json.dumps(out, ensure_ascii=False))
