"""s04 setup: Chain, the maintenance technician, up a step ladder fixing the penthouse's wall AC; dawn glows behind the glass."""
SCENE = {"title": "fix"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d = ctx.dur
    overlays = H.chip("s04-c", "!", "เชน · ช่างซ่อมบำรุง", 600, 560)
    js = L.JS + S.JS + f"""
    const ch = person({{ ...CHAIN, id: "s04-ch", extra: [...CHAIN.extra, "noArmL", "noArmR"] }});
    const sx = 520, sy = 817, sc = 0.92, loc = (x, y) => [(x - sx) / sc, (y - sy) / sc];
    const arms = armTo(ch, -1, ...loc(380, 356), -1) + armTo(ch, 1, ...loc(482, 364), -1);
    $("s04-v").innerHTML = penthouse(1200, place(ladder(520), 520, 1150, 1, "s04-lad") + place(ch.svg + toolbelt(ch) + arms, sx, sy, sc, "s04-chg")) + HEAT(0.2) + VIG;
    shot({d:.2f}, 1.08, -20, 30, [["#s04-far", 10, 0], ["#s04-mid", -6, 0], ["#s04-near", -20, 0]]);
    alive("s04-ch", ch, "s04-chg", 0, {d:.2f}, {{ armL: false, armR: false }});
    face("s04-ch", "fQ", 0.2, 0.01);
    // he works the louver loose; the unit's LED blinks, the haze outside drifts
    ft("#s04-acl", {{ y: 0 }}, {{ y: 6, duration: 0.25, yoyo: true, repeat: {max(1, int(d / 0.25) - 1)}, ease: "sine.inOut" }}, 0);
    flicker("#s04-acled", 0, {d:.2f}, 0.2, 1, 0.3);
    ft("#s04-haze", {{ y: 0 }}, {{ y: -60, duration: {d:.2f}, ease: "none" }}, 0);
    flicker("#s04-beam", 0, {d:.2f}, 0.4, 0.7, 0.6);
    pop("#s04-c", 0.35);"""
    return ctx.scene("", "", overlays, js, bg="#cdb8a6")
