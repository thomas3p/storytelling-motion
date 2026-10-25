"""s06 setup: the night buffet — a fat bag, fresh blood, a jar of trimmed tissue; napkin tucked in; the clients' receipt: paid."""
SCENE = {"title": "buffet"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, tf, tb, tm, tp = ctx.dur, ctx.t("fat"), ctx.t("blood"), ctx.t("meat"), ctx.t("pay")
    overlays = H.receipt("s06-rc", 600, 250, [("ดูดไขมัน", "฿89,000"), ("เสริมจมูก", "฿65,000"), ("ตัดหนังตา", "฿35,000")], "฿189,000")
    js = L.JS + S.JS + f"""
    const pim = person({{ ...PIM, id: "s06-pim", extra: [...PIM.extra, "noArmL", "noArmR"] }});
    const arms = armTo(pim, -1, -150, pim.shY + 170) + armTo(pim, 1, 150, pim.shY + 170);
    const forks = `<path d="M-150,${{f1(pim.shY + 170)}} L-176,${{f1(pim.shY + 60)}}" stroke="#d8dce2" stroke-width="8" stroke-linecap="round" /><path d="M-186,${{f1(pim.shY + 64)}} l0,-30 M-176,${{f1(pim.shY + 60)}} l0,-30 M-166,${{f1(pim.shY + 56)}} l0,-30" stroke="#d8dce2" stroke-width="5" stroke-linecap="round" />`
      + `<path d="M150,${{f1(pim.shY + 170)}} L176,${{f1(pim.shY + 54)}}" stroke="#d8dce2" stroke-width="10" stroke-linecap="round" />`;
    const napkin = `<path d="M-40,${{f1(pim.shY + 4)}} L40,${{f1(pim.shY + 4)}} L0,${{f1(pim.shY + 90)}} Z" fill="#ffffff" />`;
    const fat = `<g id="s06-fat"><g transform="translate(260 1180)"><path d="M-90,0 Q-110,-150 -60,-200 L60,-200 Q110,-150 90,0 Z" fill="#f2d27a" opacity="0.92" /><path d="M-90,0 Q-110,-150 -60,-200 L60,-200 Q110,-150 90,0 Z" fill="url(#s06-shade)" />`
      + `${{R(-40, -230, 80, 34, "#e8e0c8", 8)}}${{R(-58, -140, 116, 46, "#ffffff", 6)}}${{T(0, -108, 26, "#8a5a1a", "ไขมัน")}}</g></g>`;
    const blood = `<g id="s06-blood"><g transform="translate(540 1180)"><path d="M-80,0 L-80,-210 Q0,-236 80,-210 L80,0 Z" fill="#c8243a" /><path d="M-80,0 L-80,-210 Q0,-236 80,-210 L80,0 Z" fill="url(#s06-shade)" />`
      + `${{R(-52, -150, 104, 50, "#ffffff", 6)}}${{T(0, -115, 28, "#c8243a", "เลือด")}}<path d="M0,-226 Q20,-300 80,-320" stroke="#c8243a" stroke-width="8" fill="none" /></g></g>`;
    const jar = `<g id="s06-jar"><g transform="translate(810 1180)">${{R(-70, -170, 140, 170, "#dff0f4", 22, 'opacity="0.75"')}}<path d="M-40,-30 Q-50,-90 -10,-100 Q40,-110 44,-60 Q50,-20 0,-20 Z" fill="#e88a8a" />${{R(-76, -190, 152, 30, "#8a1e3c", 10)}}`
      + `${{R(-50, -150, 100, 40, "#ffffff", 6)}}${{T(0, -121, 24, "#8a1e3c", "ชิ้นเนื้อ")}}</g></g>`;
    const table = `<g id="s06-table">${{R(80, 1180, 920, 40, "#7a8690", 10)}}${{R(110, 1220, 860, 700, "#3a4650")}}${{R(110, 1220, 860, 700, "url(#s06-shadeV)")}}${{fat}}${{blood}}${{jar}}</g>`;
    $("s06-v").innerHTML = wasteRoom(true, place(pim.svg + napkin + forks + arms, 540, 1330, 1.12, "s06-pimg"), false) + table + VIG;
    face("s06-pim", "fP", 0, 0.01);
    shot({d:.2f}, 1.07, 0, -20, [["#s06-far", 10], ["#s06-mid", -6], ["#s06-table", -14]]);
    alive("s06-pim", pim, "s06-pimg", 0, {d:.2f}, {{ armL: false, armR: false }});
    flicker("#s06-tube", 0, {d:.2f}, 0.6, 1, 0.19);
    // "ถุงไขมัน เลือดสด ชิ้นเนื้อ": each dish lands on the table
    [["#s06-fat", {tf:.2f}, "260 1180"], ["#s06-blood", {tb:.2f}, "540 1180"], ["#s06-jar", {tm:.2f}, "810 1180"]].forEach(([s, t, o]) =>
      ft(s, {{ opacity: 0, scale: 0.6, y: -40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(1.8)", svgOrigin: o }}, t - 0.1));
    face("s06-pim", "fH", {tm + 0.5:.2f}, 0.15);
    // "แถมลูกค้าเป็นคนจ่ายเงิน" {tp:.2f}: the receipt
    ft("#s06-rc", {{ opacity: 0, y: -30, rotation: -4 }}, {{ opacity: 1, y: 0, rotation: 3, duration: 0.4, ease: "back.out(1.6)" }}, {tp - 0.1:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#0a0e18")
