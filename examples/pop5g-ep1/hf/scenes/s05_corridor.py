"""s05 setup: after closing, 02:13 — she walks down the dark corridor toward the waste room; her eyes turn red: the buffet."""
SCENE = {"title": "corridor"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, tb = ctx.dur, ctx.t("buffet")
    js = L.JS + S.JS + f"""
    const pim = person({{ ...PIM, id: "s05-pim" }});
    $("s05-v").innerHTML = corridor("02:13", `<g id="s05-walk">${{place(pim.svg, 540, 1190, 0.72, "s05-pimg")}}</g>`) + VIG;
    shot({d:.2f}, 1.09, 0, -30, [["#s05-far", 8], ["#s05-mid", -6], ["#s05-near", -18]]);
    alive("s05-pim", pim, "s05-pimg", 0, {d:.2f});
    flicker("#s05-tube", 0, {d:.2f}, 0.55, 1, 0.17);
    // she walks toward us
    ft("#s05-walk", {{ scale: 1, x: 0, y: 0 }}, {{ scale: 1.32, x: -173, y: -100, duration: {d:.2f}, ease: "sine.inOut" }}, 0);
    ft("#s05-pimg", {{ y: 0 }}, {{ y: -8, duration: 0.32, yoyo: true, repeat: {int(d / 0.32) - 1}, ease: "sine.inOut" }}, 0);
    // "คือบุฟเฟต์ของเธอ" {tb:.2f}: red eyes
    face("s05-pim", "fP", {tb - 0.2:.2f}, 0.25);"""
    return ctx.scene("", "", "", js, bg="#080b16")
