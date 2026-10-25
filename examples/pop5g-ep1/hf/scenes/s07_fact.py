"""s07 fact: ASPS — liposuction over 5 L (fat + fluid) should be watched overnight; a big canister fills to the 5 L line."""
SCENE = {"title": "fact"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, t6, t7, tf, to = ctx.dur, ctx.t("p6"), ctx.t("p7"), ctx.t("five"), ctx.t("overnight")
    overlays = "\n".join([H.card("s07-k1", 1, "lipo", "สมาคมศัลยแพทย์ตกแต่ง<br>อเมริกัน (ASPS)", "แนวทางความปลอดภัยการดูดไขมัน", tag="เรื่องจริง"),
                          H.stat("s07-k2", 1, "lipo", "ดูดไขมัน (รวมของเหลว) เกิน", "0", "ลิตร"),
                          H.chip("s07-c", "!", "ควรนอนเฝ้าดูอาการค้างคืน", 210, 470),
                          '    <div id="s07-src" class="fk-src">ที่มา: ASPS Practice Advisory on Liposuction</div>'])
    css = """
    .fk-src { position: absolute; left: 40px; right: 40px; top: 1168px; z-index: 18; text-align: center; font-weight: 500; font-size: 28px; color: #9fc4cf; opacity: 0; }"""
    js = L.JS + S.JS + f"""
    const marks = [1, 2, 3, 4, 5].map((i) => `<path d="M50,${{-4 - i * 52}} L90,${{-4 - i * 52}}" stroke="#5a6a70" stroke-width="4" />` + T(108, 4 - i * 52, 22, i === 5 ? "#b01c30" : "#5a7f8a", i + " L", 700, "start")).join("");
    const bg = `<rect width="1080" height="1920" fill="#0c1a20" /><g id="s07-far">${{R(0, 0, 1080, 1920, "url(#s07-shadeV)")}}${{glow(540, 860, 520, "cold", 0.18)}}</g>`;
    const can = `<g id="s07-mid"><g transform="translate(540 1180) scale(1.8)">${{R(-90, -300, 180, 300, "#e8f4f8", 30, 'opacity="0.9"')}}<clipPath id="s07-cc"><rect x="-86" y="-296" width="172" height="292" rx="26" /></clipPath>`
      + `<g clip-path="url(#s07-cc)"><rect id="s07-lvl" x="-90" y="-4" width="180" height="300" fill="#f2d27a" /></g>${{R(-90, -300, 180, 300, "url(#s07-shade)", 30)}}${{R(-50, -330, 100, 34, "#5a6a70", 10)}}${{marks}}`
      + `<path id="s07-line" d="M-110,-264 L110,-264" stroke="#e5483a" stroke-width="5" stroke-dasharray="14 10" opacity="0" /></g></g>`;
    $("s07-v").innerHTML = bg + can + VIG;
    shot({d:.2f}, 1.06, 0, -20, [["#s07-far", 8], ["#s07-mid", -10]]);
    flicker("#s07-far", 0, {d:.2f}, 0.85, 1, 0.6);
    // "รู้ไหม" {t6:.2f} … "สมาคมศัลยแพทย์ตกแต่งอเมริกันแนะนำว่า" {t7:.2f}
    cardIn("#s07-k1", {t6:.2f}, {tf - t6 - 0.35:.2f});
    ft("#s07-src", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {t7 + 0.4:.2f});
    // "ถ้าดูดไขมันเกินห้าลิตร" {tf:.2f}: count 0 → 5 while the canister fills to the line
    cardIn("#s07-k2", {tf - 0.1:.2f});
    count($("s07-k2-num"), 0, 5, {tf:.2f}, 1.4, 1);
    ft("#s07-k2-bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.4, ease: "power1.inOut" }}, {tf:.2f});
    ft("#s07-lvl", {{ y: 0 }}, {{ y: -262, duration: 1.4, ease: "power1.inOut" }}, {tf:.2f});
    ft("#s07-line", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {tf + 1.3:.2f});
    // "ควรนอนเฝ้าดูอาการค้างคืน" {to:.2f}
    pop("#s07-c", {to:.2f});"""
    return ctx.scene(css, "", overlays, js, bg="#0c1a20")
