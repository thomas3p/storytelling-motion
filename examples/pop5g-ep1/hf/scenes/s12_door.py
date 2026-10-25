"""s12 climax: Dr Pim stands smiling in the bright doorway: "the waste here never stays the night" — her eyes flash red for a beat."""
SCENE = {"title": "door"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, t14 = ctx.dur, ctx.t("p14")
    overlays = H.bubble("s12-b", "ขยะที่นี่…<br>ไม่เคยค้างคืนหรอกจ้ะ", 300, 250, 620, "c")
    js = L.JS + S.JS + f"""
    const pim = person({{ ...PIM, id: "s12-pim" }}), fon = person({{ ...FON, id: "s12-fon" }});
    const door = `<g id="s12-door">${{R(360, 420, 360, 780, "#fff6e6")}}${{glow(540, 800, 420, "warm", 0.6)}}${{cone(540, 1200, 90, 600, 60, "#fff1d6", 0.35)}}</g>`;
    $("s12-v").innerHTML = wasteRoom(false, door + place(pim.svg, 540, 1190, 0.95, "s12-pimg"), false) + place(fon.svg, 150, 1420, 1.25, "s12-fong") + VIG;
    shot({d:.2f}, 1.08, 0, -24, [["#s12-far", 10], ["#s12-mid", -6]]);
    alive("s12-pim", pim, "s12-pimg", 0, {d:.2f}); alive("s12-fon", fon, "s12-fong", 0, {d:.2f}, {{ seed: 4 }});
    flicker("#s12-door", 0, {d:.2f}, 0.88, 1, 0.5);
    face("s12-fon", "fS", 0, 0.01); face("s12-fon", "fQ", 1.4);
    // "ขยะที่นี่… ไม่เคยค้างคืนหรอกจ้ะ" {t14:.2f}: the sweet line, and a red flash in her eyes
    pop("#s12-b", {t14 - 0.1:.2f});
    face("s12-pim", "fP", {t14 + 1.2:.2f}, 0.15); face("s12-pim", "fN", {t14 + 1.9:.2f}, 0.2);"""
    return ctx.scene("", "", overlays, js, bg="#a8b8c0")
