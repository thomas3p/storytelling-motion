"""s11 climax: outside the glass, a flock of birds drops out of the white-hot sky; Chain stares, frozen."""
SCENE = {"title": "birds"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, tb = ctx.dur, ctx.t("birds")
    js = L.JS + S.JS + f"""
    const ch = person({{ ...CHAIN_HOT, id: "s11-ch" }});
    $("s11-v").innerHTML = glassView(place(ch.svg + toolbelt(ch) + sweat(ch, "s11-ch", 6), 770, 1300, 1.12, "s11-chg")) + HEAT(0.6) + VIG;
    // the birds: dark silhouettes that tumble down at staggered times
    const r = rng(5); let b = "";
    for (let i = 0; i < 9; i++) {{ const x = f1(80 + r() * 560), s = f1(0.6 + r() * 0.6);
      b += `<g id="s11-b${{i}}" transform="translate(${{x}} 0)"><g transform="scale(${{s}})"><g class="s11-bb"><path d="M-40,-6 Q-20,-26 0,-4 Q20,-26 40,-6 Q20,-12 0,6 Q-20,-12 -40,-6 Z" fill="#2a1a1a" /><circle cx="0" cy="2" r="9" fill="#2a1a1a" /></g></g></g>`; }}
    $("s11-birds").innerHTML = b;
    shot({d:.2f}, 1.08, -20, -20, [["#s11-far", 0, 14], ["#s11-mid", 0, -6], ["#s11-near", 0, -20]]);
    alive("s11-ch", ch, "s11-chg", 0, {d:.2f});
    ft("#s11-haze", {{ y: 0 }}, {{ y: -90, duration: {d:.2f}, ease: "none" }}, 0);
    flicker("#s11-sun", 0, {d:.2f}, 0.85, 1, 0.5);
    // "ฝูงนก" {tb:.2f}: they fall, spinning
    for (let i = 0; i < 9; i++) ft(`#s11-b${{i}}`, {{ y: -120, rotation: 0 }}, {{ y: 1380, rotation: (i % 2 ? 1 : -1) * (200 + i * 30), duration: 1.5 + (i % 3) * 0.25, ease: "power2.in", svgOrigin: "0 0" }}, {tb - 0.4:.2f} + i * 0.16);
    face("s11-ch", "fS", {tb + 0.2:.2f});"""
    return ctx.scene("", "", "", js, bg="#ffb070")
