"""s10 climax (phone footage, closer): she never touches the bags — yet every red bag slowly sags flat, as if something sucks
it dry from the inside; faint red wisps drift to her."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shared import FOOT_CSS, foot_svg, foot_ui

SCENE = {"title": "deflate"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, tdf = ctx.dur, ctx.t("deflate")
    js = L.JS + S.JS + f"""
    const sil = person({{ ...PIM_SIL, id: "s10-sil" }});
    const bag = (x, y, s, r, i) => `<g id="s10-b${{i}}"><g transform="translate(${{x}} ${{y}}) scale(${{s}}) rotate(${{r}})"><path d="M-70,0 Q-90,-110 -42,-146 L42,-146 Q90,-110 70,0 Z" fill="#d42a40" /><path d="M-70,0 Q-90,-110 -42,-146 L42,-146 Q90,-110 70,0 Z" fill="${{SH}}" /><path d="M-22,-146 L0,-176 L22,-146" fill="#a81c30" /></g></g>`;
    const bags = [[650, 1000, 1.25, -6], [800, 990, 1.3, 5], [930, 1010, 1.15, 9]].map(([x, y, s, r], i) => bag(x, y, s, r, i)).join("");
    const wisps = `<g id="s10-wisp" opacity="0">${{[0, 1, 2].map((i) => `<path d="M${{680 + i * 130}},${{880}} q-60,-70 -150,-60 t-180,-60" stroke="#ff8a9a" stroke-width="8" fill="none" stroke-linecap="round" opacity="${{0.75 - i * 0.15}}" />`).join("")}}</g>`;
    $("s10-v").innerHTML = wasteRoom(true, place(sil.svg, 300, 1260, 1.15, "s10-silg")) + bags + wisps + `{foot_svg("s10")}` + VIG;
    shot({d:.2f}, 1.07, 0, -24, [["#s10-far", 6], ["#s10-near", -12]]);
    alive("s10-sil", sil, "s10-silg", 0, {d:.2f});
    flicker("#s10-tube", 0, {d:.2f}, 0.4, 0.9, 0.12);
    // "แต่ถุงแดงทุกใบค่อย ๆ แฟบลง" {tdf:.2f}
    [0, 1, 2].forEach((i) => ft(`#s10-b${{i}}`, {{ scaleY: 1, scaleX: 1 }}, {{ scaleY: 0.28, scaleX: 1.12, duration: 2.6, ease: "sine.in", transformOrigin: "50% 100%" }}, {tdf - 0.1:.2f} + i * 0.25));
    ft("#s10-wisp", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 1.0, ease: "sine.out" }}, {tdf + 0.4:.2f});
    flicker("#s10-wisp", {tdf + 1.4:.2f}, {d:.2f}, 0.5, 1, 0.3);
    const ts = {{ s: 2 * 3600 + 13 * 60 + 9 }}, el = $("s10-ui-ts"), fmt = (v) => [Math.floor(v / 3600), Math.floor(v / 60) % 60, Math.floor(v) % 60].map((n) => String(n).padStart(2, "0")).join(":");
    tl.to(ts, {{ s: ts.s + {d:.0f}, duration: {d:.2f}, ease: "none", onUpdate: () => (el.textContent = fmt(ts.s)) }}, 0);"""
    return ctx.scene(FOOT_CSS, "", foot_ui("s10-ui", "02:13:09"), js, bg="#0a0e18")
