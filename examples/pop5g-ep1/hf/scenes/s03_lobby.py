"""s03 setup: หมอพิม, the star surgeon, in her clinic lobby — clients queue, the black cat on the counter, the board says next free slot: next year."""
SCENE = {"title": "lobby"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, tq = ctx.dur, ctx.t("queue")
    js = L.JS + S.JS + f"""
    const pim = person({{ ...PIM, id: "s03-pim" }});
    const ca = person({{ ...CLIENT_A, id: "s03-ca" }}), cb = person({{ ...CLIENT_B, id: "s03-cb" }}), cc = person({{ ...CLIENT_C, id: "s03-cc" }});
    $("s03-v").innerHTML = lobby()
      + `<g id="s03-q">${{place(cc.svg, 990, 1130, 0.62, "s03-ccg")}}${{place(cb.svg, 895, 1138, 0.66, "s03-cbg")}}${{place(ca.svg, 795, 1146, 0.7, "s03-cag")}}</g>`
      + place(cat({{ ...LIPO, id: "s03-cat" }}), 300, 900, 0.8, "s03-catg")
      + `<g id="s03-aura">${{[[390, 620], [700, 560], [430, 900], [680, 820]].map(([x, y]) => glow(x, y, 26, "white", 0.9)).join("")}}</g>`
      + place(pim.svg, 540, 1190, 1.0, "s03-pimg") + VIG;
    shot({d:.2f}, 1.07, 0, -20, [["#s03-far", 10], ["#s03-mid", -8], ["#s03-q", -16]]);
    alive("s03-pim", pim, "s03-pimg", 0, {d:.2f});
    alive("s03-ca", ca, "s03-cag", 0, {d:.2f}, {{ seed: 3 }}); alive("s03-cb", cb, "s03-cbg", 0, {d:.2f}, {{ seed: 5 }}); alive("s03-cc", cc, "s03-ccg", 0, {d:.2f}, {{ seed: 9 }});
    sway("#s03-cat-tail", "30 -10", 12, 0.6, 0, {int(d / 0.6) - 1}); sway("#s03-cat-hd", "0 -110", 4, 1.1, 0, {int(d / 1.1) - 1});
    blinks("s03-cat", 0, {d:.2f}, 4);
    flicker("#s03-l1", 0, {d:.2f}, 0.85, 1, 0.45); flicker("#s03-l2", 0, {d:.2f}, 0.8, 1, 0.38); flicker("#s03-l3", 0, {d:.2f}, 0.85, 1, 0.5);
    flicker("#s03-aura", 0, {d:.2f}, 0.2, 1, 0.3);
    // "คิวยาวข้ามปี" {tq:.2f}: the board pulses, the queue shuffles, Pim beams
    ft("#s03-board", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut", svgOrigin: "885 440" }}, {tq:.2f});
    face("s03-pim", "fH", {tq + 0.1:.2f}); face("s03-pim", "fN", {tq + 1.3:.2f});"""
    return ctx.scene("", "", "", js, bg="#d7bfbd")
