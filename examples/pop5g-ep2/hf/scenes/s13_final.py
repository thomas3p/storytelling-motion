"""s13 cliffhanger: outside the clinic at night Fon stops by a lamp post: a glowing sticker — "ไล่ผีออนไลน์ · อาจารย์เต้ย".
Who would you show the clip to? End screen: appointment card "ครั้งที่ 2"."""
SCENE = {"title": "final"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, t15, t_end = ctx.dur, ctx.t("p15"), ctx.t("p15.end")
    overlays = "\n".join([H.appt("s13-ap", "ใบนัด · คลินิกหมอพิม", "ครั้งที่", "2"), H.series_line("s13-sr", "ปอบยุค 5G · EP.2", "ขยะติดเชื้อ")])
    js = L.JS + S.JS + f"""
    const fon = person({{ ...FON, id: "s13-fon", extra: [...FON.extra, "noArmR"] }});
    const ph = armTo(fon, 1, 70, fon.shY + 150) + `${{R(50, f1(fon.shY + 110), 50, 80, "#15171f", 8)}}${{R(56, f1(fon.shY + 116), 38, 64, "#7fd6ff", 6, 'opacity="0.8"')}}`;
    let qr = ""; const r = rng(77); for (let y = 0; y < 7; y++) for (let x = 0; x < 7; x++) if (r() > 0.45 || (x < 2 && y < 2) || (x > 4 && y < 2) || (x < 2 && y > 4)) qr += R(902 + x * 14, 800 + y * 14, 12, 12, "#1b2440");
    const sticker = `<g id="s13-stk">${{glow(950, 880, 170, "neon", 0.55)}}${{R(880, 760, 140, 250, "#fbf3dc", 14)}}${{R(880, 760, 140, 34, "#d63a2c", 14)}}${{qr}}${{T(950, 948, 28, "#d63a2c", "ไล่ผี")}}${{T(950, 984, 28, "#1b2440", "ออนไลน์")}}</g>`;
    $("s13-v").innerHTML = clinicExt("00:41", false, place(fon.svg + ph, 470, 1190, 0.95, "s13-fong")) + sticker + VIG + `<rect id="s13-dark" width="1080" height="1920" fill="#04060a" opacity="0" />`;
    shot({d:.2f}, 1.08, 20, -24, [["#s13-far", 12], ["#s13-mid", -6], ["#s13-near", -20]]);
    alive("s13-fon", fon, "s13-fong", 0, {d:.2f}, {{ armR: false }});
    flicker("#s13-lamp", 0, {d:.2f}, 0.85, 1, 0.4); flicker("#s13-stk", 0, {d:.2f}, 0.75, 1, 0.45); flicker("#s13-mastg", 0, {d:.2f}, 0.3, 1, 0.5);
    face("s13-fon", "fQ", {t15 + 0.6:.2f});
    // end screen
    tl.to("#s13-dark", {{ opacity: 0.92, duration: 0.5, ease: "sine.inOut" }}, {t_end + 0.2:.2f});
    ft("#s13-ap", {{ opacity: 0, scale: 0.86, y: 20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(1.5)" }}, {t_end + 0.35:.2f});
    ft("#s13-sr", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {t_end + 0.45:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#070a1c")
