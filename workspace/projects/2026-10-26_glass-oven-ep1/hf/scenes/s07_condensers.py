"""s07 rising: 6:30, 44 °C — every AC unit on the service balcony runs flat out … then they blow, one after another."""
SCENE = {"title": "condensers"}


def build(ctx):
    S = ctx.lib.sets
    d, tb, tb2 = ctx.dur, ctx.t("boom"), ctx.t("boom2")
    booms = [(1, tb), (3, tb + 0.6), (5, tb2 + 0.4)]
    blow = "\n".join(f"""    // unit {n} blows at {t:.2f}
    ft("#s07-bl{n}", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1.1, duration: 0.12, ease: "power2.out", svgOrigin: "0 0" }}, {t:.2f});
    tl.to("#s07-bl{n}", {{ opacity: 0, duration: 0.45, ease: "power1.in" }}, {t + 0.18:.2f});
    ft("#s07-sm{n}", {{ opacity: 0, y: 0 }}, {{ opacity: 1, y: -160, duration: {max(0.5, d - t):.2f}, ease: "sine.out" }}, {t + 0.1:.2f});
    ft("#s07-flash", {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.06, yoyo: true, repeat: 1, ease: "none" }}, {t:.2f});
    ft("#s07-v", {{ x: 0, y: 0 }}, {{ x: 16, y: -10, duration: 0.05, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {t:.2f});""" for n, t in booms)
    stop = {n: t for n, t in booms}
    fans = "\n".join(f'    ft("#s07-fan{n}", {{ rotation: 0 }}, {{ rotation: {int(9 * stop.get(n, d)) * 360}, duration: {stop.get(n, d):.2f}, ease: "none", svgOrigin: "0 0" }}, 0);' for n in range(1, 6))
    js = S.JS + f"""
    $("s07-v").innerHTML = condensers() + HEAT(0.45) + VIG + `<rect id="s07-flash" width="1080" height="1920" fill="#fff1c8" opacity="0" />`;
    shot({d:.2f}, 1.08, 0, -20, [["#s07-far", 0, 12], ["#s07-mid", 0, -8], ["#s07-near", 0, -26]]);
    ft("#s07-haze", {{ y: 0 }}, {{ y: -90, duration: {d:.2f}, ease: "none" }}, 0);
    flicker("#s07-sun", 0, {d:.2f}, 0.85, 1, 0.5);
    // the units rattle at full power
    [1, 2, 3, 4, 5].forEach((n, i) => ft(`#s07-u${{n}}`, {{ y: 0 }}, {{ y: -3, duration: 0.07 + i * 0.01, yoyo: true, repeat: {max(1, int(d / 0.07) - 1)}, ease: "sine.inOut" }}, 0));
{fans}
{blow}"""
    return ctx.scene("", "", "", js, bg="#ff8a4a")
