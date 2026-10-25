"""s09 climax (phone footage): the door swings open by itself … a woman's silhouette in a white coat walks in and stops at the bins."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shared import FOOT_CSS, foot_svg, foot_ui

SCENE = {"title": "door"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, t10, tsh, tst = ctx.dur, ctx.t("p10"), ctx.t("shadow"), ctx.t("stop")
    js = L.JS + S.JS + f"""
    const sil = person({{ ...PIM_SIL, id: "s09-sil" }});
    const door = `${{R(120, 420, 300, 770, "#05070c")}}<g id="s09-door">${{R(120, 420, 300, 770, "#2a3446")}}${{R(120, 420, 300, 770, SH)}}<circle cx="390" cy="820" r="12" fill="#8a94a8" /></g>`;
    $("s09-v").innerHTML = wasteRoom(true, door + `<g id="s09-walk">${{place(sil.svg, 270, 1190, 0.92, "s09-silg")}}</g>`) + `{foot_svg("s09")}` + VIG;
    shot({d:.2f}, 1.05, 0, -14, [["#s09-far", 6], ["#s09-near", -10]]);
    alive("s09-sil", sil, "s09-silg", 0, {d:.2f});
    flicker("#s09-tube", 0, {d:.2f}, 0.4, 0.9, 0.11);
    ft("#s09-walk", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "sine.inOut" }}, {tsh - 0.3:.2f});
    // "ประตูเปิดเอง" {t10:.2f}: the door swings in on its hinge
    ft("#s09-door", {{ scaleX: 1 }}, {{ scaleX: 0.18, duration: 1.0, ease: "sine.inOut", svgOrigin: "120 800" }}, {t10 - 0.1:.2f});
    // "เงาผู้หญิงในชุดกาวน์" {tsh:.2f} … "เดินมาหยุดหน้าถัง" {tst:.2f}
    ft("#s09-walk", {{ x: 0 }}, {{ x: 230, duration: {tst - tsh + 0.3:.2f}, ease: "sine.inOut" }}, {tsh - 0.3:.2f});
    ft("#s09-silg", {{ y: 0 }}, {{ y: -6, duration: 0.34, yoyo: true, repeat: {max(1, int((tst - tsh + 0.3) / 0.34) - 1)}, ease: "sine.inOut" }}, {tsh - 0.3:.2f});
    // the footage clock ticks on
    const ts = {{ s: 2 * 3600 + 13 * 60 + 4 }}, el = $("s09-ui-ts"), fmt = (v) => [Math.floor(v / 3600), Math.floor(v / 60) % 60, Math.floor(v) % 60].map((n) => String(n).padStart(2, "0")).join(":");
    tl.to(ts, {{ s: ts.s + {d:.0f}, duration: {d:.2f}, ease: "none", onUpdate: () => (el.textContent = fmt(ts.s)) }}, 0);"""
    return ctx.scene(FOOT_CSS, "", foot_ui("s09-ui", "02:13:04"), js, bg="#0a0e18")
