"""s12 climax: blackout — the lift hall goes dark, the lifts die on 40; only the green EXIT sign is left: forty floors of fire
stairs. Chain heads for the stair door before his body cooks."""
SCENE = {"title": "blackout"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, tl_, ts, t40, tg = ctx.dur, ctx.t("lift"), ctx.t("stairs"), ctx.t("forty"), ctx.t("p15")
    overlays = H.chip("s12-c", "40", "บันไดหนีไฟ 40 ชั้น", 300, 400)
    js = L.JS + S.JS + f"""
    const ch = person({{ ...CHAIN_HOT, id: "s12-ch" }});
    const exit2 = `<g id="s12-exit2" transform="translate(965 480)">${{R(-80, -32, 160, 60, "#0e3a24", 8)}}${{T(0, 10, 30, "#46e070", "EXIT")}}${{glow(0, 0, 160, "green", 0.7)}}</g>`;
    $("s12-v").innerHTML = liftHall(`<g id="s12-walk">${{place(ch.svg + toolbelt(ch) + sweat(ch, "s12-ch", 6), 520, 1190, 1.0, "s12-chg")}}</g>`) + exit2 + HEAT(0.55) + VIG;
    shot({d:.2f}, 1.08, 0, -24, [["#s12-far", 0, 10], ["#s12-near", 0, -10]]);
    alive("s12-ch", ch, "s12-chg", 0, {d:.2f});
    // power dies: lights fade, the lift indicator dies, red emergency light
    ft("#s12-lights", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.5, ease: "power2.in" }}, 0.25);
    ft("#s12-dark", {{ opacity: 0 }}, {{ opacity: 0.72, duration: 0.5, ease: "power2.in" }}, 0.25);
    ft("#s12-emer", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.7);
    flicker("#s12-emer", 1.0, {d:.2f}, 0.35, 1, 0.5);
    flicker("#s12-exit2", 0, {d:.2f}, 0.8, 1, 0.4);
    // "ลิฟต์ค้าง" {tl_:.2f}
    ft("#s12-ind", {{ opacity: 1 }}, {{ opacity: 0.15, duration: 0.08, yoyo: true, repeat: 5, ease: "none" }}, {tl_:.2f});
    tl.set("#s12-indt", {{ textContent: "--" }}, {tl_ + 0.5:.2f});
    face("s12-ch", "fS", {tl_:.2f});
    // "เหลือแค่บันไดหนีไฟ" {ts:.2f} … "สี่สิบชั้น" {t40:.2f}
    face("s12-ch", "fQ", {ts:.2f});
    pop("#s12-c", {t40 - 0.2:.2f});
    // "ต้องลงถึงใต้ดิน" {tg:.2f}: he walks to the stair door and it swings open
    ft("#s12-walk", {{ x: 0 }}, {{ x: 250, duration: 1.6, ease: "sine.inOut" }}, {tg:.2f});
    ft("#s12-chg", {{ y: 0 }}, {{ y: -8, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {tg:.2f});
    ft("#s12-fdoor", {{ scaleX: 1 }}, {{ scaleX: 0.2, duration: 0.8, ease: "sine.inOut", svgOrigin: "870 860" }}, {tg + 1.1:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#a89a90")
