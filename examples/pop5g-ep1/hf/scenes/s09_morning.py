"""s09 rising: Monday morning — the new assistant nurse ฝน arrives for her first day outside the clinic (LED 07:58)."""
SCENE = {"title": "morning"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, tf = ctx.dur, ctx.t("fon")
    overlays = H.card("s09-k", "2", "nurse", "ฝน", "พยาบาลผู้ช่วยคนใหม่ · วันแรก")
    js = L.JS + S.JS + f"""
    const fon = person({{ ...FON, id: "s09-fon", extra: [...FON.extra, "noArmR"] }});
    const wave = `<g id="s09-wave">${{armTo(fon, 1, 165, fon.shY - 70, -1)}}</g>`;
    $("s09-v").innerHTML = clinicExt("07:58", true, place(fon.svg + wave, 390, 1190, 1.0, "s09-fong")) + VIG;
    shot({d:.2f}, 1.07, 0, -20, [["#s09-far", 12], ["#s09-mid", -6], ["#s09-near", -22]]);
    alive("s09-fon", fon, "s09-fong", 0, {d:.2f}, {{ armR: false }});
    flicker("#s09-mast", 0, {d:.2f}, 0.5, 1, 0.5);
    face("s09-fon", "fH", 0.2, 0.01);
    sway("#s09-wave", `${{f1(fon.ax)}} ${{f1(fon.ay)}}`, 10, 0.3, 0.2, {int((d - 0.2) / 0.3) - 1});
    // "ชื่อฝน" {tf:.2f}
    cardIn("#s09-k", {tf - 0.2:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#9fd0ec")
