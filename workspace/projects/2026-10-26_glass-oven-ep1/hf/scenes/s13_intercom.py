"""s13 cliffhanger: the wall intercom crackles — a call from basement B2 — and a whisper: "อย่าลงมา" (don't come down)."""
SCENE = {"title": "intercom"}


def build(ctx):
    S, H = ctx.lib.sets, ctx.lib.hud
    d, ti, tr, t17 = ctx.dur, ctx.t("icom"), ctx.t("ring"), ctx.t("p17")
    overlays = H.bubble("s13-b", "อย่าลงมา", 330, 250, 420, "c")
    css = """
    #s13-b { font-size: 72px; color: #c8243a; }"""
    js = S.JS + f"""
    let lines = ""; for (let y = 0; y < 1920; y += 8) lines += R(0, y, 1080, 3, "#000", 0, 'opacity="0.25"');
    $("s13-v").innerHTML = intercomWall() + `<g id="s13-scan" opacity="0">${{lines}}</g>` + VIG;
    shot({d:.2f}, 1.12, 0, -40, [["#s13-far", 0, 10], ["#s13-mid", 0, -12]]);
    flicker("#s13-emer", 0, {d:.2f}, 0.4, 1, 0.5);
    ft("#s13-led", {{ opacity: 0.15 }}, {{ opacity: 0.15, duration: 0.1 }}, 0);
    // "อินเตอร์คอม" {ti:.2f} … "ดังขึ้น" {tr:.2f}: the call LED blinks, the screen shows B2
    ft("#s13-scr", {{ opacity: 0.2 }}, {{ opacity: 1, duration: 0.08, yoyo: true, repeat: 4, ease: "none" }}, {ti:.2f});
    ft("#s13-led", {{ opacity: 0.15 }}, {{ opacity: 1, duration: 0.25, yoyo: true, repeat: {max(1, int((d - tr) / 0.25) - 1)}, ease: "sine.inOut", immediateRender: false }}, {tr - 0.1:.2f});
    // "อย่าลงมา" {t17:.2f}: the whisper, as a glitching bubble
    ft("#s13-scan", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {t17 - 0.2:.2f});
    pop("#s13-b", {t17 - 0.05:.2f});
    ft("#s13-b", {{ x: 0 }}, {{ x: 10, duration: 0.05, yoyo: true, repeat: 7, ease: "none" }}, {t17 + 0.1:.2f});
    ft("#s13-v", {{ x: 0 }}, {{ x: -8, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }}, {t17:.2f});"""
    return ctx.scene(css, "", overlays, js, bg="#0a080a")
