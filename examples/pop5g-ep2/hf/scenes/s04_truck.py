"""s04 setup: the infectious-waste truck comes every Friday — 24 pickups in six months — and every manifest says 0 kg;
the driver shrugs beside an empty cart."""
SCENE = {"title": "truck"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, t3, tz = ctx.dur, ctx.t("p3"), ctx.t("zero")
    overlays = "\n".join([H.stat("s04-k1", 2, "bin", "รถมาเก็บ · 6 เดือน", "0", "ครั้ง"), H.stat("s04-k2", 3, "book", "น้ำหนักที่ส่งให้", "0", "กก."),
                          H.chip("s04-c", "!", "ทุกครั้ง", 690, 470)])
    js = L.JS + S.JS + f"""
    const drv = person({{ ...DRIVER, id: "s04-drv", extra: [...DRIVER.extra, "noArmL", "noArmR"] }});
    const arms = armTo(drv, -1, -170, drv.shY + 40, -1) + armTo(drv, 1, 170, drv.shY + 40, -1);
    const cart = `<g id="s04-cart"><g transform="translate(180 1190)">${{R(-90, -170, 180, 130, "#8a9aa2", 10)}}${{R(-80, -160, 160, 110, "#3a4650", 8)}}<circle cx="-60" cy="-20" r="20" fill="#2a2a2e" /><circle cx="60" cy="-20" r="20" fill="#2a2a2e" />${{T(0, -90, 28, "#cfe0e8", "ว่าง")}}</g></g>`;
    $("s04-v").innerHTML = alley(cart + place(drv.svg + arms, 360, 1190, 0.95, "s04-drvg")) + `<g id="s04-puff">${{[0, 1, 2].map((i) => `<circle cx="${{1040 + i * 18}}" cy="${{1110 - i * 40}}" r="${{22 + i * 10}}" fill="#d8d8d8" opacity="0.5" />`).join("")}}</g>` + VIG;
    shot({d:.2f}, 1.07, 0, -20, [["#s04-far", 10], ["#s04-mid", -6], ["#s04-near", -16]]);
    alive("s04-drv", drv, "s04-drvg", 0, {d:.2f}, {{ armL: false, armR: false }});
    ft("#s04-truck", {{ y: 0 }}, {{ y: -3, duration: 0.12, yoyo: true, repeat: {int(d / 0.12) - 1}, ease: "sine.inOut" }}, 0);
    ft("#s04-puff", {{ y: 0, opacity: 0.8 }}, {{ y: -50, opacity: 0.2, duration: 1.2, repeat: {max(1, int(d / 1.2) - 1)}, ease: "sine.out" }}, 0);
    // "รถเก็บขยะมาทุกวันศุกร์" {t3:.2f}: 24 pickups
    cardIn("#s04-k1", {t3:.2f}, {tz - t3 - 0.35:.2f});
    count($("s04-k1-num"), 0, 24, {t3 + 0.2:.2f}, 1.2);
    ft("#s04-k1-bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.2, ease: "power1.inOut" }}, {t3 + 0.2:.2f});
    // "คือศูนย์กิโล ทุกครั้ง" {tz:.2f}
    cardIn("#s04-k2", {tz - 0.1:.2f});
    pop("#s04-c", {tz + 0.6:.2f});
    face("s04-drv", "fQ", {tz:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#9fc4dc")
