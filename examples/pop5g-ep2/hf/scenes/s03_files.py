"""s03 setup: after hours Fon sneaks into the records room and opens six months of waste manifests."""
SCENE = {"title": "files"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, tf = ctx.dur, ctx.t("file")
    overlays = H.chip("s03-c", "6", "ใบส่งขยะ · ย้อนหลัง 6 เดือน", 70, 250)
    js = L.JS + S.JS + f"""
    const fon = person({{ ...FON, id: "s03-fon", extra: [...FON.extra, "noArmL", "noArmR"] }});
    const y0 = fon.shY + 150;
    const book = `<g id="s03-book">${{R(-130, f1(y0 - 70), 130, 150, "#f4f0e6", 6)}}${{R(0, f1(y0 - 70), 130, 150, "#fbf8f0", 6)}}${{[0, 1, 2, 3].map((i) => R(-110, f1(y0 - 40 + i * 28), 90, 8, "#9aa6b0", 4) + R(20, f1(y0 - 40 + i * 28), 90, 8, "#9aa6b0", 4)).join("")}}`
      + `<g id="s03-page">${{R(0, f1(y0 - 70), 130, 150, "#ffffff", 6)}}${{R(20, f1(y0 - 30), 90, 30, "#e5483a", 6, 'opacity="0.85"')}}</g>${{R(-6, f1(y0 - 74), 12, 158, "#c8243a", 4)}}</g>`;
    const arms = armTo(fon, -1, -110, y0 + 30) + armTo(fon, 1, 110, y0 + 30);
    $("s03-v").innerHTML = records(place(fon.svg + book + arms, 520, 1190, 1.0, "s03-fong")) + VIG;
    shot({d:.2f}, 1.08, 0, -24, [["#s03-far", 12], ["#s03-mid", -6], ["#s03-near", -18]]);
    alive("s03-fon", fon, "s03-fong", 0, {d:.2f}, {{ armL: false, armR: false }});
    flicker("#s03-lamp", 0, {d:.2f}, 0.82, 1, 0.4);
    face("s03-fon", "fQ", 0, 0.01);
    // "เปิดแฟ้ม" {tf:.2f}: pages flip
    [0, 0.45, 0.9].forEach((dt) => ft("#s03-page", {{ scaleX: 1 }}, {{ scaleX: -1, duration: 0.4, ease: "sine.inOut", svgOrigin: `0 ${{f1(y0)}}` }}, {tf:.2f} + dt));
    pop("#s03-c", {tf + 0.2:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#0c0a10")
