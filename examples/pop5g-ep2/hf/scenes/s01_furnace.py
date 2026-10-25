"""s01 hook: every infectious-waste bag must end its life in the incinerator — red bags ride the belt past a roaring furnace."""
SCENE = {"title": "furnace"}


def build(ctx):
    S = ctx.lib.sets
    d = ctx.dur
    js = S.JS + f"""
    $("s01-v").innerHTML = incinerator() + VIG;
    shot({d:.2f}, 1.08, 0, -26, [["#s01-far", 12], ["#s01-mid", -6]]);
    ft("#s01-belt", {{ x: 0 }}, {{ x: 240, duration: {d:.2f}, ease: "none" }}, 0);
    flicker("#s01-fire", 0, {d:.2f}, 0.75, 1, 0.16, 0.06, "540 1060");
    flicker("#s01-fireg", 0, {d:.2f}, 0.7, 1, 0.22);
    ft("#s01-smoke", {{ y: 0, opacity: 0.8 }}, {{ y: -60, opacity: 0.4, duration: {d:.2f}, ease: "sine.inOut" }}, 0);"""
    return ctx.scene("", "", "", js, bg="#0a080a")
