"""s04 setup: by day she operates — theatre lamp, monitor, the lipo canister filling; chips: liposuction, nose job, eyelids."""
SCENE = {"title": "theatre"}


def build(ctx):
    L, S, H = ctx.lib.looks, ctx.lib.sets, ctx.lib.hud
    d, tl_, tn, te = ctx.dur, ctx.t("lipo"), ctx.t("nose"), ctx.t("eye")
    overlays = "\n".join([H.chip("s04-c1", 1, "ดูดไขมัน", 70, 250), H.chip("s04-c2", 2, "เสริมจมูก", 70, 360), H.chip("s04-c3", 3, "ตัดหนังตา", 70, 470)])
    js = L.JS + S.JS + f"""
    const pim = person({{ ...PIM_OR, id: "s04-pim", extra: [...PIM_OR.extra, "noArmL", "noArmR"] }});
    const arms = armTo(pim, -1, -70, pim.shY + 150, 1, "#bfe3ea") + armTo(pim, 1, 60, pim.shY + 160, 1, "#bfe3ea");
    const cannula = `<g id="s04-can"><path d="M60,${{f1(pim.shY + 160)}} L-40,${{f1(pim.shY + 300)}}" stroke="#c9d2d8" stroke-width="9" stroke-linecap="round" /><path d="M60,${{f1(pim.shY + 160)}} Q160,${{f1(pim.shY + 260)}} 330,${{f1(pim.shY + 200)}}" stroke="#e8f4f8" stroke-width="10" fill="none" opacity="0.7" /></g>`;
    $("s04-v").innerHTML = oroom(place(pim.svg + cannula + arms, 560, 1300, 1.05, "s04-pimg")) + VIG;
    shot({d:.2f}, 1.08, 0, -24, [["#s04-far", 12], ["#s04-mid", -6], ["#s04-near", -22]]);
    alive("s04-pim", pim, "s04-pimg", 0, {d:.2f}, {{ armL: false, armR: false }});
    flicker("#s04-lamp", 0, {d:.2f}, 0.9, 1, 0.5); flicker("#s04-ecg", 0, {d:.2f}, 0.5, 1, 0.36);
    ft("#s04-can", {{ rotation: -3 }}, {{ rotation: 4, duration: 0.5, yoyo: true, repeat: {int(d / 0.5) - 1}, ease: "sine.inOut", svgOrigin: "60 -260" }}, 0);
    // "ดูดไขมัน" {tl_:.2f}: the canister fills
    ft("#s04-fat", {{ y: 0 }}, {{ y: -150, duration: {d - tl_:.2f}, ease: "sine.inOut" }}, {tl_:.2f});
    pop("#s04-c1", {tl_ - 0.1:.2f}); pop("#s04-c2", {tn - 0.1:.2f}); pop("#s04-c3", {te - 0.1:.2f});"""
    return ctx.scene("", "", overlays, js, bg="#0c1a20")
