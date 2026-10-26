"""s02 hook: where would you run? The glass tower stands black against a swelling sun — title 60°C รุ่งอรุณเดือด."""
SCENE = {"title": "title"}


def build(ctx):
    S, H = ctx.lib.sets, ctx.lib.hud
    d, tt = ctx.dur, ctx.t("title")
    overlays = H.title("s02-ttl", "60°C", "รุ่งอรุณเดือด", 1, "แดดแรกเดือด")
    js = S.JS + f"""
    $("s02-v").innerHTML = tower(0.25) + HEAT(0.35) + VIG + `<rect id="s02-flash" width="1080" height="1920" fill="#fff1c8" opacity="0" />`;
    shot({d:.2f}, 1.1, 0, -30, [["#s02-far", 0, 14], ["#s02-mid", 0, -10], ["#s02-near", 0, -26]]);
    // the sun moves in behind the tower and swells
    ft("#s02-sun", {{ x: -300, y: 260, scale: 1 }}, {{ x: -360, y: 120, scale: 1.5, duration: {d:.2f}, ease: "sine.inOut", svgOrigin: "900 520" }}, 0);
    flicker("#s02-oven", 0, {d:.2f}, 0.2, 0.45, 0.5);
    ft("#s02-haze", {{ y: 0 }}, {{ y: -90, duration: {d:.2f}, ease: "none" }}, 0);
    // title {tt:.2f}
    ft("#s02-flash", {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.12, yoyo: true, repeat: 1, ease: "sine.out" }}, {tt - 0.05:.2f});
    ft("#s02-ttl", {{ opacity: 0, y: 24, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.5)" }}, {tt:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#3a1a3e")
