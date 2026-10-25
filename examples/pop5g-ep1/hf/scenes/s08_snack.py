"""s08 rising: but for Dr Pim, five litres is a bedtime snack — her office at night, a straw in the 5 L canister; the cat watches."""
SCENE = {"title": "snack"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, ts, ts2 = ctx.dur, ctx.t("snack"), ctx.t("snack2")
    js = L.JS + S.JS + f"""
    const pim = person({{ ...PIM, id: "s08-pim", extra: [...PIM.extra, "noArmR"] }});
    const hand = armTo(pim, 1, 150, pim.shY + 120);
    $("s08-v").innerHTML = office(place(pim.svg + hand, 600, 1190, 1.0, "s08-pimg") + place(cat({{ ...LIPO, id: "s08-cat" }}), 250, 1122, 0.7, "s08-catg")) + VIG;
    // the straw runs from the canister (780,1120) to her mouth
    const my = 1190 + pim.hy + 40, mx = 600 + 6;
    $("s08-straw").setAttribute("d", `M10,-330 L-40,-400 L${{f1(mx - 780)}},${{f1(my - 1120)}}`);
    shot({d:.2f}, 1.08, 0, -26, [["#s08-far", 14], ["#s08-mid", -6], ["#s08-near", -18]]);
    alive("s08-pim", pim, "s08-pimg", 0, {d:.2f}, {{ armR: false }});
    sway("#s08-cat-tail", "30 -10", 12, 0.7, 0, {int(d / 0.7) - 1}); sway("#s08-cat-hd", "0 -110", 5, 0.9, 0, {int(d / 0.9) - 1}); blinks("s08-cat", 0, {d:.2f}, 6);
    flicker("#s08-lamp", 0, {d:.2f}, 0.85, 1, 0.42);
    // "ห้าลิตร" {ts:.2f} … "แค่ของว่างก่อนนอน" {ts2:.2f}: she sips, blissful, and the level drops
    face("s08-pim", "fH", {ts - 0.3:.2f}, 0.2);
    ft("#s08-canfat", {{ y: 0 }}, {{ y: 200, duration: {d - ts + 0.2:.2f}, ease: "sine.in" }}, {ts - 0.2:.2f});
    face("s08-cat", "fS", {ts2:.2f}, 0.15);"""
    return ctx.scene("", "", "", js, bg="#100810")
