"""s06 setup: then the sun comes up — the first light floods through the glass wall so hot it stings; Chain shields his eyes."""
SCENE = {"title": "sunrise"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, tg, tb = ctx.dur, ctx.t("glare"), ctx.t("burn")
    js = L.JS + S.JS + f"""
    const ch = person({{ ...CHAIN, id: "s06-ch", extra: [...CHAIN.extra, "noArmR"] }});
    const down = armTo(ch, 1, ch.ax + 16, ch.ay + 176), up = armTo(ch, 1, 30, ch.hy - 14, -1);
    const body = ch.svg + toolbelt(ch) + `<g id="s06-ad">${{down}}</g><g id="s06-au" opacity="0">${{up}}</g>` + sweat(ch, "s06-ch");
    $("s06-v").innerHTML = penthouse(1220, place(body, 540, 1190, 1.0, "s06-chg"), false) + HEAT(0.3) + VIG + `<rect id="s06-white" width="1080" height="1920" fill="#fff6dc" opacity="0" />`;
    shot({d:.2f}, 1.1, 0, -30, [["#s06-far", 0, 16], ["#s06-mid", 0, -8], ["#s06-near", 0, -24]]);
    alive("s06-ch", ch, "s06-chg", 0, {d:.2f}, {{ armR: false }});
    // the sun climbs up the glass, the beams thicken
    ft("#s06-sun", {{ y: 0, scale: 1 }}, {{ y: -520, scale: 1.25, duration: {d:.2f}, ease: "sine.out", svgOrigin: "700 1220" }}, 0);
    ft("#s06-beam", {{ opacity: 0.2 }}, {{ opacity: 1, duration: {tg:.2f}, ease: "sine.in" }}, 0);
    ft("#s06-haze", {{ y: 0 }}, {{ y: -90, duration: {d:.2f}, ease: "none" }}, 0);
    ft("#s06-ch-sw", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {tb:.2f});
    // "แสงแรก" {tg:.2f}: a white glare; he throws an arm over his eyes
    ft("#s06-white", {{ opacity: 0 }}, {{ opacity: 0.6, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {tg - 0.1:.2f});
    ft("#s06-ad", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.15 }}, {tg:.2f}); ft("#s06-au", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, {tg:.2f});
    face("s06-ch", "fS", {tg:.2f});
    // "ร้อนจนแสบผิว" {tb:.2f}: the room tints hot
    ft("#s06-heat", {{ opacity: 0.3 }}, {{ opacity: 0.75, duration: 1.2, ease: "sine.inOut" }}, {tb:.2f});"""
    return ctx.scene("", "", "", js, bg="#cdb8a6")
