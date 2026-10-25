"""Scene wrapper for the survival-5styles "flood" look (tools/flatkit.js), used by tools/scenekit.py when a series lib sets
KIT = "flat" in hud.py.

scene(sid, dur, css, svg, overlays, js, bg, fade_in) -> scene HTML
- svg is drawn inside a camera group ({sid}-cam, push it with push("#{sid}-cam", ...)); reference kit defs as url(#{sid}-shade),
  url(#{sid}-shadeV), url(#{sid}-vig), url(#{sid}-g-<glow>), filter url(#{sid}-blur10) / url(#{sid}-grain).
- js runs with the kit unpacked: person, armTo, cat, glow, cone, led, place, VIG, ft, pop, cardIn, count, push, fadeIn,
  flash, face, sway, breathe, blinks, rng, f1, $ — and `tl`, the scene timeline. Characters are built in JS and dropped into
  <g> slots with $("slot").innerHTML = place(person({...}).svg, x, y, scale, "id").
- fade_in > 0 cross-dissolves the whole scene in (the previous scene keeps playing underneath for that long).
Overlays (EP tag, knowledge card, number card, appointment card, speech bubble) come from the series hud.py.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT_JS = open(os.path.join(HERE, "flatkit.js"), encoding="utf-8").read()

FONTS = """
    @font-face { font-family: "Prompt"; src: url("assets/fonts/Prompt-Bold.ttf") format("truetype"); font-weight: 700; }
    @font-face { font-family: "Prompt"; src: url("assets/fonts/Prompt-Medium.ttf") format("truetype"); font-weight: 500; }
    @font-face { font-family: "Mitr"; src: url("assets/fonts/Mitr-SemiBold.ttf") format("truetype"); font-weight: 600; }"""

UNPACK = "const { P, $, f1, D, rng, addDef, SH, SHV, glowDef, glow, cone, led, person, armTo, cat, ft, pop, cardIn, count, push, fadeIn, flash, face, sway, breathe, blinks, place, VIG, shot, alive, flicker } = K;"


def scene(sid, dur, css, svg, overlays, js, bg="#05070d", fade_in=0.0, grain=0.07):
    fade = (f'    tl.fromTo("#{sid}-fade", {{ opacity: 0 }}, {{ opacity: 1, duration: {fade_in}, ease: "none" }}, 0);' if fade_in else "")
    grain_svg = (f'      <svg class="fk-full" viewBox="0 0 1080 1920" width="1080" height="1920" style="position: absolute; z-index: 30; pointer-events: none">'
                 f'<rect width="1080" height="1920" filter="url(#{sid}-grain)" opacity="{grain}" /></svg>' if grain else "")
    return f"""<template>
  <style>{FONTS}
    #root {{ position: absolute; inset: 0; overflow: hidden; background: transparent; font-family: "Prompt", sans-serif; color: #fff; }}
    #root svg {{ display: block; overflow: visible; }}
    .fk-full {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #{sid}-cam {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px 900px; }}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <svg width="0" height="0" style="position: absolute"><defs id="{sid}-defs"></defs></svg>
    <div id="{sid}-fade" class="fk-full" style="background: {bg}">
      <div id="{sid}-cam"><svg id="{sid}-v" viewBox="0 0 1080 1920" width="1080" height="1920">
{svg}
      </svg></div>
{overlays}
{grain_svg}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{KIT_JS}
    const K = FLATKIT("{sid}", tl);
    {UNPACK}
{js}
{fade}
    tl.to({{}}, {{ duration: {dur} }}, 0);
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
