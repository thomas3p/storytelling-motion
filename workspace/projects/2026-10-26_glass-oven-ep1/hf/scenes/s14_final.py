"""s14 cliffhanger: would you go down? The fire stairs from above — forty floors spiralling into a red glow. End screen: the lift
floor indicator stuck at 40, goal basement B2, next episode."""
SCENE = {"title": "final"}


def build(ctx):
    S, H = ctx.lib.sets, ctx.lib.hud
    d, t18, t_end = ctx.dur, ctx.t("p18"), ctx.t("p18.end")
    overlays = "\n".join([H.floor_card("s14-fl", "ตอนนี้อยู่ชั้น", "", "เป้าหมาย: ชั้นใต้ดิน B2"),
                          H.series_line("s14-sr", "60°C รุ่งอรุณเดือด · EP.1 แดดแรกเดือด", "ตอนต่อไป: ปล่องไฟแนวตั้ง")])
    js = S.JS + f"""
    $("s14-v").innerHTML = stairWell() + VIG + `<rect id="s14-dark" width="1080" height="1920" fill="#04060a" opacity="0" />`;
    $("s14-fl-led").innerHTML = led("40", 120, "#ff4636").svg;
    shot({d:.2f}, 1.25, 0, 0, [["#s14-far", 0, 0]]);
    ft("#s14-far", {{ rotation: 0 }}, {{ rotation: 8, duration: {d:.2f}, ease: "sine.inOut", svgOrigin: "540 900" }}, 0);
    flicker("#s14-deep", 0, {d:.2f}, 0.55, 1, 0.55, 0.12, "540 900");
    flicker("#s14-lamp", 0, {d:.2f}, 0.3, 1, 0.2);
    // end screen after "จะลงไปไหม" {t_end:.2f}
    tl.to("#s14-dark", {{ opacity: 0.9, duration: 0.5, ease: "sine.inOut" }}, {t_end + 0.2:.2f});
    ft("#s14-fl", {{ opacity: 0, scale: 0.86, y: 20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(1.5)" }}, {t_end + 0.35:.2f});
    ft("#s14-sr", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {t_end + 0.5:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#0a0808")
