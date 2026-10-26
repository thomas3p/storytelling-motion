"""s09 rising: this whole glass tower is a car left in the sun — the tower again, glowing from inside like an oven."""
SCENE = {"title": "oven"}


def build(ctx):
    S = ctx.lib.sets
    d, to = ctx.dur, ctx.t("oven")
    js = S.JS + f"""
    $("s09-v").innerHTML = tower(0) + HEAT(0.45) + VIG;
    shot({d:.2f}, 1.14, 0, 60, [["#s09-far", 0, 12], ["#s09-mid", 0, -10], ["#s09-near", 0, -20]]);
    ft("#s09-sun", {{ scale: 1.2 }}, {{ scale: 1.6, duration: {d:.2f}, ease: "sine.inOut", svgOrigin: "900 520" }}, 0);
    ft("#s09-haze", {{ y: 0 }}, {{ y: -100, duration: {d:.2f}, ease: "none" }}, 0);
    flicker("#s09-haze", 0, {d:.2f}, 0.5, 1, 0.35);
    // "ก็คือรถตากแดด" {to:.2f}: the glass glows from inside
    ft("#s09-oven", {{ opacity: 0.1 }}, {{ opacity: 1, duration: 1.4, ease: "sine.inOut" }}, {to - 0.6:.2f});
    flicker("#s09-oven", {to + 0.9:.2f}, {d:.2f}, 0.75, 1, 0.3);
    ft("#s09-heat", {{ opacity: 0.4 }}, {{ opacity: 0.8, duration: 1.4 }}, {to - 0.4:.2f});"""
    return ctx.scene("", "", "", js, bg="#3a1a3e")
