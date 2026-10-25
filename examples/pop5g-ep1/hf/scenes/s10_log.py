"""s10 rising: her first job — check the infectious-waste bins; the log says 12 kg went in yesterday."""
SCENE = {"title": "log"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, tb, tk = ctx.dur, ctx.t("bin"), ctx.t("kg12")
    overlays = "\n".join([H.card("s10-k1", 3, "bin", "งานแรกของฝน", "เช็กถังขยะติดเชื้อทุกเช้า"), H.stat("s10-k2", 4, "book", "บันทึก · ทิ้งเมื่อวาน", "0", "กก.")])
    js = L.JS + S.JS + f"""
    const fon = person({{ ...FON, id: "s10-fon", extra: [...FON.extra, "noArmL", "noArmR"] }});
    const board = `<g id="s10-board">${{R(-70, fon.shY + 60, 140, 180, "#c8a060", 10)}}${{R(-58, fon.shY + 76, 116, 150, "#ffffff", 4)}}${{[0, 1, 2, 3].map((i) => R(-44, fon.shY + 100 + i * 30, 88, 8, "#9aa6b0", 4)).join("")}}${{R(-24, fon.shY + 52, 48, 18, "#5a6068", 4)}}</g>`;
    const arms = armTo(fon, -1, -60, fon.shY + 180) + armTo(fon, 1, 60, fon.shY + 170);
    $("s10-v").innerHTML = wasteRoom(false, place(fon.svg + board + arms, 330, 1190, 1.0, "s10-fong")) + VIG;
    shot({d:.2f}, 1.07, 0, -20, [["#s10-far", 10], ["#s10-mid", -6], ["#s10-near", -20]]);
    alive("s10-fon", fon, "s10-fong", 0, {d:.2f}, {{ armL: false, armR: false }});
    flicker("#s10-tube", 0, {d:.2f}, 0.85, 1, 0.31);
    // "เช็กถังขยะติดเชื้อ" {tb:.2f}
    cardIn("#s10-k1", {tb - 0.6:.2f}, {tk - tb + 0.25:.2f});
    // "เมื่อวานทิ้งไปสิบสองกิโล" {tk:.2f}
    cardIn("#s10-k2", {tk - 0.2:.2f});
    count($("s10-k2-num"), 0, 12, {tk - 0.1:.2f}, 1.0);
    ft("#s10-k2-bar", {{ scaleX: 0 }}, {{ scaleX: 0.85, duration: 1.0, ease: "power1.inOut" }}, {tk - 0.1:.2f});
    face("s10-fon", "fQ", {tk + 0.3:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#a8b8c0")
