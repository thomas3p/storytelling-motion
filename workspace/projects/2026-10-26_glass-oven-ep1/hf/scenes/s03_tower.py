"""s03 setup: 6 a.m., the 40th floor of an all-glass luxury condo — the tower from outside, floor 40 lights up."""
SCENE = {"title": "tower"}


def build(ctx):
    S, H = ctx.lib.sets, ctx.lib.hud
    d, tf, tg = ctx.dur, ctx.t("f40"), ctx.t("glass")
    overlays = H.chip("s03-c", "40", "ชั้น 40 · ผนังกระจกทั้งหลัง", 250, 400)
    js = S.JS + f"""
    $("s03-v").innerHTML = tower(0) + `<path id="s03-glint" d="M330,240 L420,240 L330,700 Z" fill="#ffffff" opacity="0" />` + HEAT(0.2) + VIG;
    shot({d:.2f}, 1.08, 0, 40, [["#s03-far", 0, 10], ["#s03-mid", 0, -14], ["#s03-near", 0, -24]]);
    ft("#s03-haze", {{ y: 0 }}, {{ y: -80, duration: {d:.2f}, ease: "none" }}, 0);
    flicker("#s03-sun", 0, {d:.2f}, 0.85, 1, 0.6);
    // "ชั้นสี่สิบ" {tf:.2f}: the floor band lights and the chip lands
    ft("#s03-f40", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "sine.out" }}, {tf - 0.15:.2f});
    flicker("#s03-f40", {tf + 0.2:.2f}, {d:.2f}, 0.6, 1, 0.35);
    pop("#s03-c", {tf + 0.05:.2f});
    // "คอนโดหรูกระจก" {tg:.2f}: a glint runs down the glass
    ft("#s03-glint", {{ opacity: 0, x: 0 }}, {{ opacity: 0.35, x: 360, duration: 0.9, ease: "sine.inOut" }}, {tg - 0.2:.2f});
    tl.to("#s03-glint", {{ opacity: 0, duration: 0.3 }}, {tg + 0.7:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#3a1a3e")
