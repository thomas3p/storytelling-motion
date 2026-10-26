"""s10 climax: 7:00, 51 °C — Chain opens the bathroom tap; the water comes out boiling, steam blooms, he jerks back."""
SCENE = {"title": "tap"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, tt, tbo = ctx.dur, ctx.t("tap"), ctx.t("boil")
    js = L.JS + S.JS + f"""
    const ch = person({{ ...CHAIN_HOT, id: "s10-ch", extra: [...CHAIN_HOT.extra, "noArmR"] }});
    const sx = 470, sy = 1190, reach = armTo(ch, 1, (705 - sx), (742 - sy));
    const body = ch.svg + toolbelt(ch) + `<g id="s10-arm">${{reach}}</g>` + sweat(ch, "s10-ch", 6);
    $("s10-v").innerHTML = bathroom(`<g id="s10-wrap">${{place(body, sx, sy, 1.0, "s10-chg")}}</g>`) + HEAT(0.55) + VIG;
    shot({d:.2f}, 1.09, 30, -20, [["#s10-far", 10, 0], ["#s10-mid", -6, 0]]);
    alive("s10-ch", ch, "s10-chg", 0, {d:.2f}, {{ armR: false }});
    flicker("#s10-win", 0, {d:.2f}, 0.8, 1, 0.4);
    // "น้ำจากก๊อก" {tt:.2f}: water runs
    ft("#s10-water", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.2 }}, {tt - 0.3:.2f});
    ft("#s10-bub", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {tt:.2f});
    ft("#s10-bub", {{ y: 0 }}, {{ y: -8, duration: 0.09, yoyo: true, repeat: {max(1, int((d - tt) / 0.09) - 1)}, ease: "sine.inOut" }}, {tt:.2f});
    // "เดือดปุด ๆ" {tbo:.2f}: steam blooms, he jerks back
    ft("#s10-steam", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: -60, duration: 1.2, ease: "sine.out" }}, {tbo - 0.6:.2f});
    flicker("#s10-steam", {tbo + 0.7:.2f}, {d:.2f}, 0.6, 1, 0.45);
    face("s10-ch", "fS", {tbo:.2f});
    ft("#s10-wrap", {{ x: 0 }}, {{ x: -70, duration: 0.35, ease: "back.out(2)" }}, {tbo:.2f});
    ft("#s10-arm", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.2 }}, {tbo:.2f});
    ft("#s10-ch-sw", {{ y: 0 }}, {{ y: 14, duration: 0.6, yoyo: true, repeat: {max(1, int(d / 0.6) - 1)}, ease: "sine.inOut" }}, 0);"""
    return ctx.scene("", "", "", js, bg="#b8c8cc")
