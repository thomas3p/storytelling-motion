"""s02 hook: but the red bags from Dr Pim's clinic never reach the furnace — a route map: clinic → truck → incinerator,
the line breaks and a red X lands on the furnace; title."""
SCENE = {"title": "route"}


def build(ctx):
    S, H = ctx.lib.sets, ctx.lib.hud
    d, tn, tt = ctx.dur, ctx.t("never"), ctx.t("title")
    overlays = H.title("s02-ttl", "ปอบยุค 5G", 2, "ขยะติดเชื้อ")
    js = S.JS + f"""
    let grid = ""; for (let x = 0; x <= 1080; x += 60) grid += `<path d="M${{x}},0 L${{x}},1920" stroke="#1c2a44" stroke-width="2" />`; for (let y = 0; y <= 1920; y += 60) grid += `<path d="M0,${{y}} L1080,${{y}}" stroke="#1c2a44" stroke-width="2" />`;
    const clinic = `<g transform="translate(230 900)">${{R(-120, -260, 240, 260, "#2a2238", 16)}}${{R(-120, -260, 240, 260, SH, 16)}}${{R(-100, -240, 200, 60, "#1a1424", 10)}}${{T(0, -198, 30, "#ff9cc2", "คลินิกหมอพิม")}}${{glow(0, -210, 140, "neon", 0.5)}}${{R(-70, -160, 140, 120, "#ffd0e0", 8, 'opacity="0.8"')}}</g>`;
    const furnace = `<g transform="translate(850 900)">${{R(-110, -230, 220, 230, "#3a3036", 16)}}${{R(-70, -150, 140, 110, "#140a08", 14)}}${{glow(0, -100, 140, "amber", 0.9)}}${{R(40, -380, 50, 160, "#2a2226")}}${{T(0, 60, 30, "#ffb547", "เตาเผา")}}</g>`;
    const path = `<path id="s02-path" d="M330,820 Q540,620 760,820" stroke="#7fd6ff" stroke-width="10" fill="none" stroke-dasharray="26 18" stroke-linecap="round" />`;
    const truck = `<g id="s02-truck"><g transform="translate(330 800)">${{R(-50, -60, 100, 60, "#f4f4f0", 10)}}${{R(-80, -44, 34, 44, "#e8e8e4", 6)}}<circle cx="-50" cy="4" r="14" fill="#2a2a2e" /><circle cx="30" cy="4" r="14" fill="#2a2a2e" />${{bio(10, -30, 0.55, "#c8243a")}}</g></g>`;
    const cross = `<g id="s02-x" opacity="0"><path d="M760,560 L940,760 M940,560 L760,760" stroke="#e5483a" stroke-width="34" stroke-linecap="round" /></g>`;
    $("s02-v").innerHTML = `<rect width="1080" height="1920" fill="#0b1224" /><g id="s02-far">${{grid}}</g><g id="s02-mid">${{clinic}}${{furnace}}${{path}}${{truck}}${{cross}}</g>` + VIG;
    shot({d:.2f}, 1.06, 0, -20, [["#s02-far", 14], ["#s02-mid", -8]]);
    flicker("#s02-mid", 0, {d:.2f}, 0.92, 1, 0.5);
    ft("#s02-path", {{ strokeDashoffset: 0 }}, {{ strokeDashoffset: -176, duration: {d:.2f}, ease: "none" }}, 0);
    // the truck sets off along the route … and stalls halfway
    ft("#s02-truck", {{ x: 0, y: 0 }}, {{ x: 200, y: -120, duration: {tn - 0.2:.2f}, ease: "sine.inOut" }}, 0.1);
    // "ไม่เคยไปถึงเตาเลยสักใบ" {tn:.2f}: the line turns red and a cross lands on the furnace
    tl.to("#s02-path", {{ stroke: "#e5483a", duration: 0.25 }}, {tn:.2f});
    ft("#s02-x", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", svgOrigin: "850 660" }}, {tn + 0.1:.2f});
    ft("#s02-truck", {{ rotation: 0 }}, {{ rotation: -6, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut", svgOrigin: "330 800" }}, {tn:.2f});
    ft("#s02-ttl", {{ opacity: 0, y: 20, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)" }}, {tt:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#0b1224")
