"""s13 cliffhanger: that night outside the clinic a young man in a red yant headband raises his hand and sniffs the air;
his phone app reads the blood smell."""
SCENE = {"title": "tey"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, tm, ts = ctx.dur, ctx.t("man"), ctx.t("sniff")
    overlays = H.stat("s13-k", "!", "drop", "แอปดมผี · กลิ่นคาวเลือด", "0", "%")
    js = L.JS + S.JS + f"""
    const tey = person({{ ...TEY, id: "s13-tey", extra: [...TEY.extra, "noArmL", "noArmR"] }});
    const armUp = `<g id="s13-up">${{armTo(tey, 1, 175, tey.hy - 10, -1)}}</g>`;
    const phone = armTo(tey, -1, -110, tey.shY + 150) + `<g id="s13-ph">${{R(-150, f1(tey.shY + 90), 60, 100, "#15171f", 10)}}${{R(-144, f1(tey.shY + 98), 48, 84, "#ff3d7f", 6, 'opacity="0.85"')}}${{glow(-120, tey.shY + 140, 90, "neon", 0.7)}}</g>`;
    const wisps = `<g id="s13-wisp" opacity="0">${{[0, 1, 2].map((i) => `<path d="M${{900 - i * 60}},${{520 + i * 40}} q-80,40 -160,0 t-160,10 t-120,60" stroke="#ff6fae" stroke-width="7" fill="none" stroke-linecap="round" opacity="${{0.7 - i * 0.18}}" />`).join("")}}</g>`;
    $("s13-v").innerHTML = street(wisps + `<g id="s13-in">${{place(tey.svg + phone + armUp, 540, 1400, 1.18, "s13-teyg")}}</g>`) + VIG;
    shot({d:.2f}, 1.08, 0, -26, [["#s13-far", 16], ["#s13-mid", -8], ["#s13-near", -20]]);
    alive("s13-tey", tey, "s13-teyg", 0, {d:.2f}, {{ armL: false, armR: false }});
    flicker("#s13-bokeh", 0, {d:.2f}, 0.7, 1, 0.55); flicker("#s13-lamp", 0, {d:.2f}, 0.85, 1, 0.4); flicker("#s13-ph", 0, {d:.2f}, 0.75, 1, 0.3);
    // "มีผู้ชายคนหนึ่ง" {tm:.2f}: he steps into the light
    ft("#s13-in", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power2.out" }}, {tm - 0.6:.2f});
    ft("#s13-up", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {ts - 0.2:.2f});
    // "ยกมือขึ้นดมอากาศ" {ts:.2f}: the smell drifts in, the app spikes
    ft("#s13-wisp", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 1.2, ease: "sine.out" }}, {ts - 0.6:.2f});
    cardIn("#s13-k", {ts - 0.1:.2f});
    count($("s13-k-num"), 0, 98, {ts:.2f}, 1.1);
    ft("#s13-k-bar", {{ scaleX: 0 }}, {{ scaleX: 0.98, duration: 1.1, ease: "power1.inOut" }}, {ts:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#0a0a1c")
