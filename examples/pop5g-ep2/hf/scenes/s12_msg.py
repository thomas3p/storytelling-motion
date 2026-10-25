"""s12 cliffhanger: Fon, phone in hand at the nurse station — a message pops up: "ขอบคุณที่ช่วยถ่ายให้นะจ๊ะ" from หมอพิม."""
SCENE = {"title": "message"}


def build(ctx):
    L, S = ctx.lib.looks, ctx.lib.sets
    d, tm = ctx.dur, ctx.t("msg")
    overlays = ('    <div id="s12-n" class="nt"><div class="nh"><span class="av"></span><span>ข้อความ · <b>หมอพิม</b></span><em>ตอนนี้</em></div>'
                '<div class="nb">ขอบคุณที่ช่วยถ่ายให้นะจ๊ะ ♥</div></div>')
    css = """
    .nt { position: absolute; left: 90px; right: 90px; top: 250px; z-index: 18; padding: 20px 26px 26px; border-radius: 30px; background: rgba(251, 243, 220, 0.97); box-shadow: 0 18px 44px rgba(0, 0, 0, 0.5); opacity: 0; }
    .nh { display: flex; align-items: center; gap: 14px; font-size: 30px; color: #3f4e6c; font-weight: 500; }
    .nh b { color: #1b2440; font-weight: 700; } .nh em { margin-left: auto; font-style: normal; font-size: 28px; color: #6a7890; }
    .av { width: 54px; height: 54px; border-radius: 50%; background: radial-gradient(circle at 50% 38%, #f5d6bd 0 12px, transparent 13px), radial-gradient(circle at 50% 100%, #f7f5f1 0 22px, transparent 23px), #8a1e3c; }
    .nb { margin-top: 12px; font-size: 50px; font-weight: 700; color: #c8243a; line-height: 1.3; }"""
    js = L.JS + S.JS + f"""
    const fon = person({{ ...FON, id: "s12-fon", extra: [...FON.extra, "noArmL", "noArmR"] }});
    const ph = `<g id="s12-ph">${{R(-40, f1(fon.shY + 90), 80, 130, "#15171f", 12)}}${{R(-32, f1(fon.shY + 100), 64, 108, "#7fd6ff", 8, 'opacity="0.85"')}}<g id="s12-phg">${{glow(0, fon.shY + 150, 120, "cold", 0.6)}}</g></g>`;
    const arms = armTo(fon, -1, -36, fon.shY + 190) + armTo(fon, 1, 36, fon.shY + 190);
    $("s12-v").innerHTML = station(place(fon.svg + ph + arms, 540, 1290, 1.05, "s12-fong")) + VIG;
    shot({d:.2f}, 1.08, 0, -24, [["#s12-far", 10], ["#s12-mid", -6], ["#s12-near", -16]]);
    alive("s12-fon", fon, "s12-fong", 0, {d:.2f}, {{ armL: false, armR: false }});
    flicker("#s12-tube", 0, {d:.2f}, 0.6, 1, 0.23); flicker("#s12-pc", 0, {d:.2f}, 0.85, 1, 0.4);
    face("s12-fon", "fQ", 0, 0.01);
    // "มือถือของฝนก็เด้งข้อความขึ้นมา" {tm:.2f}
    ft("#s12-ph", {{ x: 0 }}, {{ x: 4, duration: 0.05, yoyo: true, repeat: 7, ease: "none" }}, {tm - 0.2:.2f});
    ft("#s12-n", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }}, {tm - 0.1:.2f});
    flicker("#s12-phg", {tm:.2f}, {d:.2f}, 0.5, 1, 0.3);
    face("s12-fon", "fS", {tm + 0.3:.2f});"""
    return ctx.scene(css, "", overlays, js, bg="#05070e")
