"""s08 fact: a study of cars parked in the sun (McLaren, Null & Quinn, Pediatrics 2005): the cabin warms ~3.2 °F (≈1.8 °C) every
5 minutes on average, and 80% of the rise comes in the first 30 minutes — a red sedan, its cabin thermometer climbing."""
SCENE = {"title": "fact"}


def build(ctx):
    S, H = ctx.lib.sets, ctx.lib.hud
    d, t8, tc, t2, t5, th = ctx.dur, ctx.t("p8"), ctx.t("car"), ctx.t("two"), ctx.t("five"), ctx.t("half")
    overlays = "\n".join([H.card("s08-k1", 1, "car", "งานวิจัยรถจอดตากแดด", "วารสาร Pediatrics ปี 2005", tag="เรื่องจริง"),
                          H.stat("s08-k2", 1, "thermo", "ในรถร้อนขึ้นเฉลี่ย ทุก 5 นาที", "0", "°C"),
                          H.chip("s08-c", "%", "80% ของความร้อน มาใน 30 นาทีแรก", 110, 560),
                          H.src("s08-src", "ที่มา: McLaren, Null &amp; Quinn · Pediatrics 116(1), 2005")])
    js = S.JS + f"""
    $("s08-v").innerHTML = carlot() + HEAT(0.35) + VIG;
    shot({d:.2f}, 1.07, 0, -24, [["#s08-far", 0, 10], ["#s08-mid", 0, -10], ["#s08-near", 0, -20]]);
    ft("#s08-haze", {{ y: 0 }}, {{ y: -70, duration: {d:.2f}, ease: "none" }}, 0);
    flicker("#s08-haze", 0, {d:.2f}, 0.5, 1, 0.4);
    flicker("#s08-sun", 0, {d:.2f}, 0.85, 1, 0.55);
    // the cabin thermometer climbs the whole time, fastest at first (80% in the first half)
    ft("#s08-merc", {{ scaleY: 0.25 }}, {{ scaleY: 1, duration: {d:.2f}, ease: "power2.out", svgOrigin: "0 34" }}, 0);
    // "รู้ไหม" {t8:.2f}: the study card
    cardIn("#s08-k1", {t8:.2f}, {t2 - t8 - 0.55:.2f});
    ft("#s08-src", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {tc:.2f});
    // "เกือบสององศา" {t2:.2f} … "ทุกห้านาที" {t5:.2f}
    cardIn("#s08-k2", {t2 - 0.35:.2f});
    count($("s08-k2-num"), 0, 1.8, {t2 - 0.2:.2f}, 1.0, 1);
    ft("#s08-k2-bar", {{ scaleX: 0 }}, {{ scaleX: 0.8, duration: 1.0, ease: "power1.inOut" }}, {t2 - 0.2:.2f});
    // "ครึ่งชั่วโมงแรก" {th:.2f}
    pop("#s08-c", {ctx.t("p10") - 0.1:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#ffb070")
