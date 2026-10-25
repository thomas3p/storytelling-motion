"""s06 rising: but here the waste vanishes before it ever meets a flame — red bags heaped on the bins melt away into the dark."""
SCENE = {"title": "vanish"}


def build(ctx):
    S = ctx.lib.sets
    d, tv = ctx.dur, ctx.t("vanish")
    js = S.JS + f"""
    const bag = (x, y, s, r) => `<g transform="translate(${{x}} ${{y}}) scale(${{s}}) rotate(${{r}})"><path d="M-60,0 Q-76,-90 -36,-122 L36,-122 Q76,-90 60,0 Z" fill="#d42a40" /><path d="M-60,0 Q-76,-90 -36,-122 L36,-122 Q76,-90 60,0 Z" fill="${{SH}}" /><path d="M-18,-122 L0,-150 L18,-122" fill="#a81c30" /></g>`;
    const bags = [[600, 980, 1.0, -8], [690, 960, 1.1, 6], [840, 1010, 0.95, -4], [920, 990, 1.0, 10], [640, 1060, 0.9, 4]].map(([x, y, s, r], i) => `<g class="s06-bag" id="s06-b${{i}}">${{bag(x, y, s, r)}}</g>`).join("");
    const puffs = [[620, 900], [700, 880], [860, 920], [930, 900], [650, 980]].map(([x, y], i) => `<g id="s06-p${{i}}" opacity="0">${{glow(x, y, 70, "red", 0.7)}}</g>`).join("");
    $("s06-v").innerHTML = wasteRoom(true) + bags + puffs + VIG;
    shot({d:.2f}, 1.09, 0, -30, [["#s06-far", 10], ["#s06-mid", -6], ["#s06-near", -18]]);
    flicker("#s06-tube", 0, {d:.2f}, 0.45, 1, 0.13);
    // "ขยะหายไปก่อนจะได้เจอไฟ" {tv:.2f}: one by one the bags shrink into the dark
    [0, 1, 2, 3, 4].forEach((i) => {{
      const t = {tv:.2f} + i * 0.22;
      ft(`#s06-b${{i}}`, {{ opacity: 1, scale: 1 }}, {{ opacity: 0, scale: 0.4, duration: 0.6, ease: "power2.in", transformOrigin: "50% 100%" }}, t);
      ft(`#s06-p${{i}}`, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut" }}, t + 0.35);
    }});"""
    return ctx.scene("", "", "", js, bg="#0a0e18")
