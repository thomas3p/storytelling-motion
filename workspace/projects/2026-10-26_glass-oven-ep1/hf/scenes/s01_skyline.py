"""s01 hook: what if tomorrow morning the air went from 35 to 60 °C in two hours? Dawn over the city, the sun climbing,
a roadside billboard counting the temperature up from 35 to 60."""
SCENE = {"title": "skyline"}


def build(ctx):
    S = ctx.lib.sets
    d, t35, t60 = ctx.dur, ctx.t("t35"), ctx.t("t60")
    js = S.JS + f"""
    $("s01-v").innerHTML = skyline() + HEAT(0.15) + VIG;
    shot({d:.2f}, 1.09, 0, -36, [["#s01-far", 0, 18], ["#s01-mid", 0, -8], ["#s01-near", 0, -30]]);
    ft("#s01-sun", {{ y: 160 }}, {{ y: -90, duration: {d:.2f}, ease: "sine.out" }}, 0);
    ft("#s01-haze", {{ y: 0 }}, {{ y: -110, duration: {d:.2f}, ease: "none" }}, 0);
    flicker("#s01-haze", 0, {d:.2f}, 0.5, 1, 0.45);
    // "สามสิบห้า" {t35:.2f} → "หกสิบ" {t60:.2f}: the billboard races up and turns the frame hot
    const o = {{ v: 35 }}, el = $("s01-btemp");
    tl.fromTo(o, {{ v: 35 }}, {{ v: 60, duration: {t60 - t35 + 0.4:.2f}, ease: "power2.in", onUpdate: () => (el.textContent = Math.round(o.v) + "°C") }}, {t35:.2f});
    ft("#s01-heat", {{ opacity: 0.2 }}, {{ opacity: 0.7, duration: {t60 - t35 + 0.8:.2f}, ease: "power1.in" }}, {t35:.2f});
    ft("#s01-btemp", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.18, yoyo: true, repeat: 1, ease: "sine.inOut", svgOrigin: "180 150" }}, {t60 + 0.3:.2f});"""
    return ctx.scene("", "", "", js, bg="#24123a")
