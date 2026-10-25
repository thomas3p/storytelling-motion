"""s02 hook: Pop of the 5G age — the city at night, a 5G mast pulsing, the clinic's pink neon sign and its LED clock 23:47; title."""
SCENE = {"title": "city"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, tg, tc = ctx.dur, ctx.t("g5"), ctx.t("clinic")
    overlays = H.title("s02-ttl", "ปอบยุค 5G", 1, "บุฟเฟต์ถูกกฎหมาย")
    js = L.JS + S.JS + f"""
    $("s02-v").innerHTML = clinicExt("23:47") + VIG;
    shot({d:.2f}, 1.08, 0, -30, [["#s02-far", 12], ["#s02-mid", -6], ["#s02-near", -24]]);
    flicker("#s02-mastg", 0, {d:.2f}, 0.3, 1, 0.5); flicker("#s02-mast", 0, {d:.2f}, 0.4, 1, 0.5);
    flicker("#s02-lamp", 0, {d:.2f}, 0.85, 1, 0.4); flicker("#s02-winglow", 0, {d:.2f}, 0.75, 1, 0.6);
    // "ยุคห้าจี" {tg:.2f}: the mast sends out rings
    [1, 2, 3].forEach((i) => ft(`#s02-w${{i}}`, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, yoyo: true, repeat: {max(1, int((d - tg) / 0.5) - 1)}, ease: "sine.inOut" }}, {tg:.2f} + i * 0.12));
    // "เปิดคลินิกศัลยกรรม" {tc:.2f}: the neon buzzes on, the title lands
    ft("#s02-neon", {{ opacity: 0.25 }}, {{ opacity: 1, duration: 0.08, yoyo: true, repeat: 4, ease: "sine.inOut" }}, {tc - 0.3:.2f});
    ft("#s02-ttl", {{ opacity: 0, y: 20, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)" }}, {tc + 0.1:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#070a1c")
