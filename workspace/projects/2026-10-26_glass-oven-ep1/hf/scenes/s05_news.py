"""s05 setup: last night's breaking news on the penthouse TV — the ozone layer over the city has torn; a hole opens on the globe."""
SCENE = {"title": "news"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, toz, trip = ctx.dur, ctx.t("ozone"), ctx.t("rip")
    overlays = H.news("s05-n", "ข่าวด่วน", "ชั้นโอโซนเหนือเมืองฉีกขาด")
    js = L.JS + S.JS + f"""
    const an = person({{ ...NEWS, id: "s05-an" }});
    let lines = ""; for (let y = 140; y < 1180; y += 6) lines += R(60, y, 960, 2, "#000", 0, 'opacity="0.18"');
    const studio = `<rect width="1080" height="1920" fill="#0a0c12" />
      <g id="s05-far">${{R(60, 140, 960, 1040, "#16305a")}}${{glow(540, 560, 520, "cold", 0.35)}}
        <g transform="translate(700 560)"><circle r="230" fill="#2a6ab0" /><path d="M-150,-120 Q-60,-170 30,-110 Q110,-60 60,30 Q-20,90 -90,40 Q-170,-10 -150,-120 Z" fill="#4aa070" /><path d="M60,90 Q140,60 180,130 Q120,190 60,150 Z" fill="#4aa070" />
          <circle r="230" fill="none" stroke="#9fd0ff" stroke-width="18" opacity="0.6" />
          <g id="s05-hole" opacity="0">${{glow(-30, -60, 220, "red", 0.95)}}<path d="M-110,-90 Q-60,-150 10,-120 Q80,-80 40,-20 Q0,30 -70,10 Q-140,-20 -110,-90 Z" fill="#3a0a2a" opacity="0.85" /></g></g></g>
      <g id="s05-mid">${{place(an.svg, 330, 1480, 1.35, "s05-ang")}}${{R(60, 1000, 960, 180, "#1b2440")}}${{R(60, 1000, 960, 12, "#e5483a")}}${{T(860, 1060, 34, "#ffffff", "NEWS 24", 700)}}</g>
      ${{lines}}<g id="s05-near">${{R(0, 0, 1080, 140, "#05060a")}}${{R(0, 1180, 1080, 740, "#05060a")}}${{R(0, 0, 60, 1920, "#05060a")}}${{R(1020, 0, 60, 1920, "#05060a")}}</g>`;
    $("s05-v").innerHTML = studio + VIG;
    shot({d:.2f}, 1.07, 0, -20, [["#s05-far", 6, 0], ["#s05-mid", -6, 0]]);
    alive("s05-an", an, "s05-ang", 0, {d:.2f});
    cardIn("#s05-n", 0.2);
    // "ชั้นโอโซน" {toz:.2f} … "ฉีกขาด" {trip:.2f}: a red hole tears open over the city
    ft("#s05-hole", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.7, ease: "back.out(1.4)", svgOrigin: "-30 -60" }}, {toz:.2f});
    flicker("#s05-hole", {toz + 0.8:.2f}, {d:.2f}, 0.75, 1, 0.3);
    face("s05-an", "fS", {trip:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#0a0c12")
