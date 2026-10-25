"""s14 cliffhanger: Fon alone at the nurse station at night — would you keep working here? Behind the glass, two red eyes open.
End screen: appointment card "ครั้งที่ 1" + series line."""
SCENE = {"title": "final"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, t16, t_end = ctx.dur, ctx.t("p16"), ctx.t("p16.end")
    overlays = "\n".join([H.appt("s14-ap", "ใบนัด · คลินิกหมอพิม", "ครั้งที่", "1"), H.series_line("s14-sr", "ปอบยุค 5G · EP.1", "บุฟเฟต์ถูกกฎหมาย")])
    js = L.JS + S.JS + f"""
    const fon = person({{ ...FON, id: "s14-fon" }});
    $("s14-v").innerHTML = station(place(fon.svg, 540, 1290, 1.0, "s14-fong")) + VIG + `<rect id="s14-dark" width="1080" height="1920" fill="#04060a" opacity="0" />`;
    shot({d:.2f}, 1.08, 0, -24, [["#s14-far", 10], ["#s14-mid", -6], ["#s14-near", -16]]);
    alive("s14-fon", fon, "s14-fong", 0, {d:.2f});
    flicker("#s14-tube", 0, {d:.2f}, 0.6, 1, 0.23); flicker("#s14-pc", 0, {d:.2f}, 0.85, 1, 0.4);
    face("s14-fon", "fQ", {t16 + 0.4:.2f});
    // behind the glass, two red eyes open
    ft("#s14-eyes", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "sine.inOut" }}, {t16 + 1.3:.2f});
    // end screen
    tl.to("#s14-dark", {{ opacity: 0.92, duration: 0.5, ease: "sine.inOut" }}, {t_end + 0.2:.2f});
    ft("#s14-ap", {{ opacity: 0, scale: 0.86, y: 20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(1.5)" }}, {t_end + 0.35:.2f});
    ft("#s14-sr", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {t_end + 0.45:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#05070e")
