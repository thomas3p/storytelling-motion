"""s07 rising: Wednesday night Fon hides her phone on a shelf in the waste room and presses record (red REC light)."""
SCENE = {"title": "hide"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, th, tr = ctx.dur, ctx.t("hide"), ctx.t("rec")
    js = L.JS + S.JS + f"""
    const fon = person({{ ...FON, id: "s07-fon", extra: [...FON.extra, "noArmL"] }});
    const reach = `<g id="s07-arm">${{armTo(fon, -1, -150, -560, 1)}}</g>`;
    const shelf = `${{R(110, 660, 300, 22, "#5a6476", 6)}}${{R(130, 682, 14, 50, "#4a5466")}}${{R(376, 682, 14, 50, "#4a5466")}}${{R(130, 600, 60, 60, "#e8e8e8", 6)}}${{R(340, 610, 50, 50, "#f2c14e", 6)}}`;
    const phone = `<g id="s07-ph"><g transform="translate(262 660)">${{R(-34, -78, 68, 78, "#15171f", 10)}}${{R(-26, -70, 52, 50, "#1e2a3a", 6)}}<circle id="s07-rec" cx="0" cy="-12" r="7" fill="#ff3030" opacity="0" /></g></g>`;
    $("s07-v").innerHTML = wasteRoom(true, shelf + phone + place(fon.svg + reach, 420, 1190, 1.0, "s07-fong")) + `<g id="s07-recg" opacity="0">${{glow(262, 648, 60, "red", 0.9)}}</g>` + VIG;
    shot({d:.2f}, 1.08, -10, -30, [["#s07-far", 10], ["#s07-mid", -6], ["#s07-near", -18]]);
    alive("s07-fon", fon, "s07-fong", 0, {d:.2f}, {{ armL: false }});
    flicker("#s07-tube", 0, {d:.2f}, 0.55, 1, 0.21);
    face("s07-fon", "fQ", 0, 0.01);
    // "ฝนซ่อนมือถือไว้บนชั้น" {th:.2f}: the phone slides onto the shelf, the arm follows
    ft("#s07-ph", {{ x: 60, y: 40, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.6, ease: "power2.out" }}, {th - 0.3:.2f});
    ft("#s07-arm", {{ rotation: 6 }}, {{ rotation: 0, duration: 0.6, ease: "power2.out", svgOrigin: `${{f1(-fon.ax)}} ${{f1(fon.ay)}}` }}, {th - 0.3:.2f});
    // "กดอัดวิดีโอ" {tr:.2f}: REC
    tl.to("#s07-rec", {{ opacity: 1, duration: 0.1 }}, {tr:.2f});
    flicker("#s07-recg", {tr:.2f}, {d:.2f}, 0.2, 1, 0.5);
    face("s07-fon", "fH", {tr + 0.3:.2f});"""
    return ctx.scene("", "", "", js, bg="#0a0e18")
