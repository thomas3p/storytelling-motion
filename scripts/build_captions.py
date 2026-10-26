"""Write a HyperFrames captions scene from timings.json (tools/align_script.py output).

usage: python build_captions.py timings.json out.html [--skip 25,..] [--hl "word=#hex" ...]
One group per phrase, one group visible at a time, hard kill after each exit. A "|" in the display text breaks the line there.
"""
import argparse, html, json, re

ap = argparse.ArgumentParser()
ap.add_argument("timings"); ap.add_argument("out")
ap.add_argument("--skip", default="", help="phrase indexes shown by the scene itself")
ap.add_argument("--hl", nargs="*", default=[], help="word=#color highlights")
ap.add_argument("--top", type=int, default=1140)
ap.add_argument("--size", type=int, default=60)
ap.add_argument("--last-until", type=float, default=None, help="hold the final caption until this time (the film's last line)")
ap.add_argument("--style", default="kanit", choices=["kanit", "flood"], help="flood = Prompt, soft shadow, highlights as red pills (survival-5styles look)")
ap.add_argument("--overrides", default=None, help='JSON {"<phrase>": {"shift": s, "hold": s, "hide": true, "text": "..."}} to retime or replace single captions')
a = ap.parse_args()

phr = json.load(open(a.timings, encoding="utf-8"))["phrases"]
skip = {int(x) for x in a.skip.split(",") if x}
if a.overrides:
    for k, o in json.load(open(a.overrides, encoding="utf-8")).items():
        p = phr[int(k)]
        p["start"] = p["start"] + o.get("shift", 0)
        p["end"] = p["end"] + o.get("shift", 0) + o.get("hold", 0)
        if "text" in o:
            p["display"] = o["text"]
        if o.get("hide"):
            skip.add(int(k))
hl = [h.split("=", 1) for h in a.hl]

def mark(text):
    t = html.escape(text)
    for word, col in hl:
        w = html.escape(word)
        if w in t:
            if a.style == "flood":
                t = t.replace(w, f'<span class="hl" style="background:{col}">{w}</span>', 1)
            else:
                t = t.replace(w, f'<span style="color:{col};white-space:nowrap">{w}</span>', 1)
    # "|" in the display text is a manual line break (Thai has no spaces, so the browser may wrap mid-word)
    return t.replace("|", "<br>")

groups, js = [], []
shown = [i for i in range(len(phr)) if i not in skip]
for n, i in enumerate(shown):
    p = phr[i]
    start = max(0.12, p["start"] - 0.05)
    nxt = phr[shown[n + 1]]["start"] - 0.04 if n + 1 < len(shown) else p["end"] + 1.5
    end = round(min(nxt, p["end"] + 0.35), 3)
    if n + 1 == len(shown) and a.last_until: end = a.last_until
    gid = f"cap-{i:02d}"
    groups.append(f'    <div id="{gid}" class="cap"><span class="cap-t">{mark(p.get("display", p["text"]))}</span></div>')
    if a.style == "flood":
        js.append(f'    tl.fromTo("#{gid}", {{ opacity: 0, y: 16, scale: 0.97 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.2, ease: "power2.out" }}, {start:.3f});')
    else:
        js.append(f'    tl.fromTo("#{gid}", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.13, ease: "power4.out" }}, {start:.3f});')
    js.append(f'    tl.to("#{gid}", {{ opacity: 0, duration: 0.12, ease: "power2.in" }}, {end - 0.12:.3f});')
    js.append(f'    tl.set("#{gid}", {{ opacity: 0, visibility: "hidden" }}, {end:.3f});')

FLOOD_CSS = f"""
    @font-face {{ font-family: "Prompt"; src: url("assets/fonts/Prompt-Bold.ttf"); font-weight: 700; }}
    #root {{ position: absolute; inset: 0; pointer-events: none; font-family: "Prompt", sans-serif; }}
    .cap {{ position: absolute; left: 40px; right: 40px; top: {a.top}px; text-align: center; text-wrap: balance; opacity: 0; overflow: visible; }}
    .cap-t {{ font-size: {a.size}px; font-weight: 700; line-height: 1.4; color: #ffffff; text-shadow: 0 3px 0 rgba(0, 0, 0, 0.5), 0 0 22px rgba(0, 0, 0, 0.75); }}
    .hl {{ display: inline-block; color: #ffffff; padding: 0 16px 6px; margin: 0 4px; border-radius: 14px; text-shadow: none; box-shadow: 0 4px 0 rgba(0, 0, 0, 0.28); white-space: nowrap; }}"""
doc = f'''<template>
  <style>
    @font-face {{ font-family: "Kanit"; src: url("assets/fonts/Kanit-Bold.ttf"); font-weight: 700; }}
    #root {{ position: absolute; inset: 0; pointer-events: none; font-family: "Kanit", sans-serif; }}
    .cap {{ position: absolute; left: 0; right: 0; top: {a.top}px; padding: 0 90px; text-align: center; text-wrap: balance; opacity: 0; overflow: visible; }}
    .cap-t {{ font-size: {a.size}px; font-weight: 700; line-height: 1.32; color: #ffffff;
      -webkit-text-stroke: 10px rgba(5, 6, 10, 0.88); paint-order: stroke fill;
      text-shadow: 0 6px 24px rgba(0, 0, 0, 0.85); }}
  </style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">
{chr(10).join(groups)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["caps"] = tl;
  </script>
</template>
'''
if a.style == "flood":
    doc = re.sub(r"<style>.*?</style>", lambda m: "<style>" + FLOOD_CSS + chr(10) + "  </style>", doc, count=1, flags=re.S)
open(a.out, "w", encoding="utf-8").write(doc)
print(f"{len(shown)} caption groups -> {a.out}")
