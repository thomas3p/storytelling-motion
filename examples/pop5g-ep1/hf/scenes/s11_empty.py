"""s11 climax: she lifts the lid — the bin is empty and spotless, gleaming as if someone licked it clean; 12 → 0 kg."""
SCENE = {"title": "empty"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, te, tk = ctx.dur, ctx.t("empty"), ctx.t("lick")
    overlays = H.stat("s11-k", 4, "bin", "ในถังตอนนี้", "12", "กก.", pct=0.85)
    js = L.JS + S.JS + f"""
    const fon = person({{ ...FON, id: "s11-fon" }});
    const star = ([x, y]) => `<path d="M${{x}},${{y - 10}} L${{x + 3}},${{y - 3}} L${{x + 10}},${{y}} L${{x + 3}},${{y + 3}} L${{x}},${{y + 10}} L${{x - 3}},${{y + 3}} L${{x - 10}},${{y}} L${{x - 3}},${{y - 3}} Z" fill="#ffffff" />`;
    const big = `<g id="s11-mid2"><g transform="translate(470 1220) scale(2.0)"><path d="M-80,0 L-70,-210 L70,-210 L80,0 Z" fill="#c8243a" /><path d="M-80,0 L-70,-210 L70,-210 L80,0 Z" fill="url(#s11-shade)" />`
      + `<ellipse cx="0" cy="-210" rx="70" ry="22" fill="#eef4f6" /><ellipse cx="0" cy="-206" rx="58" ry="15" fill="#ffffff" />`
      + `<g id="s11-lid"><path d="M-86,-206 L-84,-232 Q0,-246 84,-232 L86,-206 Z" fill="#a81c30" /></g>`
      + `<g id="s11-spk">${{[[-30, -226], [26, -232], [6, -218], [44, -214]].map(star).join("")}}</g></g></g>`;
    $("s11-v").innerHTML = wasteRoom(false, place(fon.svg, 830, 1190, 0.95, "s11-fong"), false) + big + `<g id="s11-glint" opacity="0">${{glow(470, 790, 200, "white", 0.8)}}</g>` + VIG;
    shot({d:.2f}, 1.1, 0, -40, [["#s11-far", 10], ["#s11-mid2", -14]]);
    alive("s11-fon", fon, "s11-fong", 0, {d:.2f});
    flicker("#s11-tube", 0, {d:.2f}, 0.8, 1, 0.27);
    // the lid swings open
    ft("#s11-lid", {{ rotation: 0 }}, {{ rotation: -38, duration: 0.55, ease: "power2.out", svgOrigin: "-84 -214" }}, 0.25);
    cardIn("#s11-k", 0.4);
    // "แต่ถังกลับว่างเปล่า" {te:.2f}: 12 → 0
    count($("s11-k-num"), 12, 0, {te:.2f}, 0.9);
    ft("#s11-k-bar", {{ scaleX: 0.85 }}, {{ scaleX: 0, duration: 0.9, ease: "power1.inOut" }}, {te:.2f});
    face("s11-fon", "fS", {te + 0.1:.2f});
    // "สะอาดเหมือนมีใครเลีย" {tk:.2f}: it gleams
    ft("#s11-glint", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {tk - 0.1:.2f});
    ft("#s11-spk", {{ opacity: 0.2 }}, {{ opacity: 1, duration: 0.25, yoyo: true, repeat: {max(1, int((d - tk) / 0.25) - 1)}, ease: "sine.inOut" }}, {tk - 0.2:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#a8b8c0")
