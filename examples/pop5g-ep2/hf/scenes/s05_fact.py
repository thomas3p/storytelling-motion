"""s05 fact: by Thai ministerial regulation an infectious-waste incinerator burns at no less than 760 °C, then burns the smoke
again at 1,000 °C — a two-chamber cross-section lights up chamber by chamber."""
SCENE = {"title": "fact"}


def build(ctx):
    S, H = ctx.lib.sets, ctx.lib.hud
    d, t4, t5, t7, t1k = ctx.dur, ctx.t("p4"), ctx.t("p5"), ctx.t("t760"), ctx.t("t1000")
    overlays = "\n".join([H.card("s05-k1", 1, "bin", "กฎกระทรวงว่าด้วยการกำจัด<br>มูลฝอยติดเชื้อ พ.ศ. 2545", "เตาเผาต้องมี 2 ห้อง", tag="เรื่องจริง"),
                          H.stat("s05-k2", 1, "bin", "ห้องเผามูลฝอย · ไม่ต่ำกว่า", "0", "°C"),
                          H.chip("s05-c", "2", "ห้องเผาควัน ≥ 1,000°C", 300, 470),
                          '    <div id="s05-src" class="fk-src">ที่มา: กฎกระทรวงว่าด้วยการกำจัดมูลฝอยติดเชื้อ พ.ศ. 2545 · กรมควบคุมมลพิษ</div>'])
    css = """
    .fk-src { position: absolute; left: 30px; right: 30px; top: 1168px; z-index: 18; text-align: center; font-weight: 500; font-size: 28px; color: #c9a87a; opacity: 0; white-space: nowrap; }"""
    js = S.JS + f"""
    const flames = (x, y, w, c1, c2) => [0, 1, 2].map((i) => {{ const fx = x - w / 3 + i * w / 3, h = 90 + (i % 2) * 40; return `<path d="M${{fx - 40}},${{y}} Q${{fx - 30}},${{y - h}} ${{fx}},${{y - h * 1.5}} Q${{fx + 30}},${{y - h}} ${{fx + 40}},${{y}} Z" fill="${{c1}}" /><path d="M${{fx - 20}},${{y}} Q${{fx - 14}},${{y - h * 0.6}} ${{fx}},${{y - h}} Q${{fx + 14}},${{y - h * 0.6}} ${{fx + 20}},${{y}} Z" fill="${{c2}}" />`; }}).join("");
    const ch1 = `<g>${{R(110, 680, 420, 420, "#3a3036", 26)}}${{R(140, 710, 360, 360, "#120a08", 20)}}<g id="s05-f1" opacity="0.15">${{glow(320, 960, 240, "amber", 0.9)}}${{flames(320, 1060, 300, "#ffb547", "#fff1b0")}}</g>${{T(320, 1150, 30, "#ffb547", "ห้องเผา 760°C")}}</g>`;
    const ch2 = `<g>${{R(570, 580, 400, 360, "#3a3036", 26)}}${{R(600, 610, 340, 300, "#0a0a14", 20)}}<g id="s05-f2" opacity="0.15">${{glow(770, 830, 220, "cold", 0.9)}}${{flames(770, 900, 280, "#9fd0ff", "#ffffff")}}</g>${{T(770, 990, 30, "#9fd0ff", "ห้องเผาควัน 1,000°C")}}</g>`;
    const pipe = `${{R(500, 760, 100, 60, "#4a4046")}}${{R(820, 330, 90, 260, "#2a2226")}}<g id="s05-smoke">${{[0, 1, 2].map((i) => `<circle cx="${{865 + i * 24}}" cy="${{300 - i * 50}}" r="${{40 + i * 16}}" fill="#5a5258" opacity="0.4" />`).join("")}}</g>`;
    $("s05-v").innerHTML = `<rect width="1080" height="1920" fill="#120c10" /><g id="s05-far">${{R(0, 0, 1080, 1920, "url(#s05-shadeV)")}}${{glow(540, 860, 560, "red", 0.12)}}</g><g id="s05-mid">${{pipe}}${{ch1}}${{ch2}}</g>` + VIG;
    shot({d:.2f}, 1.06, 0, -24, [["#s05-far", 8], ["#s05-mid", -10]]);
    ft("#s05-smoke", {{ y: 0, opacity: 0.7 }}, {{ y: -70, opacity: 0.3, duration: {d:.2f}, ease: "sine.inOut" }}, 0);
    // "รู้ไหม" {t4:.2f} … "ตามกฎกระทรวง" {t5:.2f}
    cardIn("#s05-k1", {t4:.2f}, {t7 - t4 - 0.35:.2f});
    ft("#s05-src", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {t5 + 0.4:.2f});
    // "เจ็ดร้อยหกสิบองศา" {t7:.2f}: chamber one roars
    cardIn("#s05-k2", {t7 - 0.2:.2f});
    count($("s05-k2-num"), 0, 760, {t7 - 0.1:.2f}, 1.2);
    ft("#s05-k2-bar", {{ scaleX: 0 }}, {{ scaleX: 0.76, duration: 1.2, ease: "power1.inOut" }}, {t7 - 0.1:.2f});
    ft("#s05-f1", {{ opacity: 0.15 }}, {{ opacity: 1, duration: 0.8, ease: "sine.out" }}, {t7 - 0.1:.2f});
    flicker("#s05-f1", {t7 + 0.8:.2f}, {d:.2f}, 0.8, 1, 0.17);
    // "เผาควันซ้ำที่หนึ่งพันองศา" {t1k:.2f}: chamber two flares white-blue
    pop("#s05-c", {t1k - 0.8:.2f});
    ft("#s05-f2", {{ opacity: 0.15 }}, {{ opacity: 1, duration: 0.8, ease: "sine.out" }}, {t1k - 0.1:.2f});
    flicker("#s05-f2", {t1k + 0.8:.2f}, {d:.2f}, 0.8, 1, 0.15);"""
    return ctx.scene(css, "", overlays, js, bg="#120c10")
