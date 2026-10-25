"""s01 hook: the old days — a village night, torches, and a Pop granny chasing a raw chicken down the path."""
SCENE = {"title": "village"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d = ctx.dur
    js = L.JS + S.JS + f"""
    const g = person({{ ...GRANNY, id: "s01-gr", extra: ["noArmL", "noArmR"] }});
    const arms = armTo(g, -1, -175, g.shY + 150) + armTo(g, 1, -105, g.shY + 175);
    $("s01-v").innerHTML = village() + `<g id="s01-run">${{place(g.svg + arms, 640, 1190, 0.95, "s01-grg")}}</g>`
      + `<g id="s01-henw">${{place(hen(), 330, 1205, 1.0, "s01-hen")}}</g>` + VIG;
    face("s01-gr", "fP", 0, 0.01);
    // smooth rules: push-in + parallax, the granny breathes and sways, torches flicker
    shot({d:.2f}, 1.08, 0, -24, [["#s01-far", 14], ["#s01-mid", -10], ["#s01-near", -30]]);
    alive("s01-gr", g, "s01-grg", 0, {d:.2f}, {{ armL: false, armR: false, body: 2 }});
    flicker(".s01-fl", 0, {d:.2f}, 0.7, 1, 0.21, 0.12, "0 0");
    flicker("#s01-mid", 0, {d:.2f}, 0.85, 1, 0.33);
    // the chase: the hen scurries left, flapping; the granny lurches after it
    ft("#s01-henw", {{ x: 0 }}, {{ x: -230, duration: {d:.2f}, ease: "sine.inOut" }}, 0);
    ft("#s01-hen", {{ y: 0 }}, {{ y: -16, duration: 0.18, yoyo: true, repeat: {int(d / 0.18) - 1}, ease: "sine.inOut" }}, 0);
    sway("#s01-wing", "-30 -60", 18, 0.12, 0, {int(d / 0.12) - 1});
    ft("#s01-run", {{ x: 0 }}, {{ x: -120, duration: {d:.2f}, ease: "sine.inOut" }}, 0);
    ft("#s01-grg", {{ y: 0 }}, {{ y: -10, duration: 0.3, yoyo: true, repeat: {int(d / 0.3) - 1}, ease: "sine.inOut" }}, 0);"""
    return ctx.scene("", "", "", js, bg="#140f28")
