"""s08 rising: next morning, the phone in her hands — eight hours of black footage scrubbing by … until 02:13 (red LED)."""
SCENE = {"title": "phone"}


def build(ctx):
    S = ctx.lib.sets
    d, t8, td, t9, t213 = ctx.dur, ctx.t("p8"), ctx.t("dark"), ctx.t("p9"), ctx.t("t213")
    overlays = '    <div id="s08-tc" class="tc">00:00:00</div>'
    css = """
    .tc { position: absolute; left: 300px; width: 480px; top: 1010px; z-index: 17; text-align: center; font-family: "Mitr", sans-serif; font-weight: 600; font-size: 44px; color: #cfe0e8; letter-spacing: 2px; }"""
    js = S.JS + f"""
    const L2 = led("02:13", 120, "#ff4636");
    const phone = `<g id="s08-mid"><g transform="translate(540 820)">${{R(-270, -470, 540, 940, "#15171f", 60)}}${{R(-250, -450, 500, 900, "#05070a", 44)}}
      <g id="s08-noise" opacity="0.5">${{Array.from({{ length: 60 }}, (_, i) => R(-240 + (i * 83) % 480, -440 + (i * 151) % 880, 6, 6, "#2a3442")).join("")}}</g>
      <g id="s08-led" opacity="0"><g transform="translate(${{-L2.w / 2}} -60)"><g filter="url(#s08-blur10)" opacity="0.8">${{L2.svg}}</g>${{L2.svg}}</g></g>
      ${{R(-220, 250, 440, 10, "#2a3442", 5)}}<rect id="s08-bar" x="-220" y="250" width="440" height="10" rx="5" fill="#e5483a" />
      <path d="M-30,330 L30,360 L-30,390 Z" fill="#cfe0e8" /></g>
      <ellipse cx="270" cy="1240" rx="90" ry="70" fill="#eab48e" /><ellipse cx="810" cy="1240" rx="90" ry="70" fill="#eab48e" /></g>`;
    $("s08-v").innerHTML = `<rect width="1080" height="1920" fill="#1a1e26" /><g id="s08-far">${{glow(540, 700, 600, "cold", 0.18)}}${{R(0, 1300, 1080, 620, "#101318")}}</g>` + phone + VIG;
    shot({d:.2f}, 1.07, 0, -20, [["#s08-far", 10], ["#s08-mid", -8]]);
    flicker("#s08-noise", 0, {d:.2f}, 0.2, 0.6, 0.09);
    // "คลิปยาวแปดชั่วโมง… มีแต่ความมืด" {t8:.2f}: the timecode races, the bar crawls
    tl.set("#s08-bar", {{ scaleX: 0, transformOrigin: "0% 50%" }}, 0);
    const tc = {{ s: 0 }}, el = $("s08-tc"), fmt = (v) => [Math.floor(v / 3600), Math.floor(v / 60) % 60, Math.floor(v) % 60].map((n) => String(n).padStart(2, "0")).join(":");
    tl.to(tc, {{ s: 2 * 3600 + 13 * 60, duration: {t9 - t8 + 0.4:.2f}, ease: "power1.in", onUpdate: () => (el.textContent = fmt(tc.s)) }}, {t8 - 0.1:.2f});
    tl.to("#s08-bar", {{ scaleX: 0.28, transformOrigin: "0% 50%", duration: {t9 - t8 + 0.4:.2f}, ease: "power1.in" }}, {t8 - 0.1:.2f});
    // "จนถึงตีสองสิบสาม" {t213:.2f}: it stops — red 02:13
    tl.to("#s08-tc", {{ color: "#ff4636", duration: 0.2 }}, {t213 - 0.2:.2f});
    ft("#s08-led", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.8)", svgOrigin: "540 820" }}, {t213 - 0.2:.2f});
    flicker("#s08-led", {t213 + 0.3:.2f}, {d:.2f}, 0.55, 1, 0.3);"""
    return ctx.scene(css, "", overlays, js, bg="#1a1e26")
