"""s11 climax (phone footage, close): the silhouette turns to the camera … and smiles — two red eyes, a fang, a glitch."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shared import FOOT_CSS, foot_svg, foot_ui

SCENE = {"title": "turn"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, ttn, tsm = ctx.dur, ctx.t("turn"), ctx.t("smile")
    js = L.JS + S.JS + f"""
    const sil = person({{ ...PIM_SIL, id: "s11-sil" }});
    // seen from behind first: a hair sheet covers the face, then it turns
    const back = `<g id="s11-back"><ellipse cx="0" cy="${{f1(sil.hy - 4)}}" rx="70" ry="80" fill="#0a080c" /></g>`;
    const ex = (dx) => f1(540 + dx * 2.1), ey = f1(1720 + (sil.hy + 8) * 2.1);
    const eyes = `<g id="s11-eyeg" opacity="0">${{glow(ex(-24), ey, 84, "eye", 0.95)}}${{glow(ex(24), ey, 84, "eye", 0.95)}}<ellipse cx="${{ex(-24)}}" cy="${{ey}}" rx="19" ry="17" fill="#ff2a2a" /><ellipse cx="${{ex(24)}}" cy="${{ey}}" rx="19" ry="17" fill="#ff2a2a" /><ellipse cx="${{ex(-24)}}" cy="${{ey}}" rx="5" ry="15" fill="#2a0606" /><ellipse cx="${{ex(24)}}" cy="${{ey}}" rx="5" ry="15" fill="#2a0606" /></g>`;
    $("s11-v").innerHTML = wasteRoom(true, "", false) + place(sil.svg + back, 540, 1720, 2.1, "s11-silg") + `{foot_svg("s11")}` + eyes + `<rect id="s11-glitch" width="1080" height="1920" fill="#ff3030" opacity="0" />` + VIG;
    shot({d:.2f}, 1.1, 0, -40, [["#s11-far", 6], ["#s11-mid", -6]]);
    alive("s11-sil", sil, "s11-silg", 0, {d:.2f});
    flicker("#s11-tube", 0, {d:.2f}, 0.35, 0.85, 0.1);
    // "หันมามองกล้อง" {ttn:.2f}
    ft("#s11-back", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.45, ease: "sine.inOut" }}, {ttn - 0.1:.2f});
    ft("#s11-silg", {{ rotation: -4 }}, {{ rotation: 0, duration: 0.5, ease: "sine.inOut", svgOrigin: "0 0" }}, {ttn - 0.1:.2f});
    // "และยิ้ม" {tsm:.2f}
    face("s11-sil", "fP", {tsm - 0.1:.2f}, 0.15);
    ft("#s11-eyeg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {tsm - 0.1:.2f});
    ft("#s11-glitch", {{ opacity: 0 }}, {{ opacity: 0.22, duration: 0.06, yoyo: true, repeat: 3, ease: "none" }}, {tsm:.2f});
    const ts = {{ s: 2 * 3600 + 13 * 60 + 14 }}, el = $("s11-ui-ts"), fmt = (v) => [Math.floor(v / 3600), Math.floor(v / 60) % 60, Math.floor(v) % 60].map((n) => String(n).padStart(2, "0")).join(":");
    tl.to(ts, {{ s: ts.s + {d:.0f}, duration: {d:.2f}, ease: "none", onUpdate: () => (el.textContent = fmt(ts.s)) }}, 0);"""
    return ctx.scene(FOOT_CSS, "", foot_ui("s11-ui", "02:13:14"), js, bg="#0a0e18")
