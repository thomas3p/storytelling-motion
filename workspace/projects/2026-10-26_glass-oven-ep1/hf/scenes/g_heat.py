"""Global heat chip (top right): the clock and the temperature climb with the story (06:00 · 35°C → 07:05 · 52°C)."""
SCENE = {"title": "heat"}

# (cue, minutes after 06:00, °C) — each key eases in over ~1 s from its cue
KEYS = [("p2-0.3", 0, 35), ("glare", 12, 38), ("full", 30, 44), ("tap", 60, 51), ("lift", 64, 52), ("ring", 65, 52)]


def build(ctx):
    H = ctx.lib.hud
    sid = ctx.sid
    keys = [(max(0.05, ctx.t(c)), m, t) for c, m, t in KEYS]
    tw = "\n".join(
        f'    tl.fromTo(st, {{ m: {a[1]}, t: {a[2]} }}, {{ m: {b[1]}, t: {b[2]}, duration: 1.1, ease: "power1.inOut", immediateRender: false, onUpdate: draw }}, {b[0]:.2f});'
        for a, b in zip(keys, keys[1:]))
    js = f"""
    const st = {{ m: 0, t: 35 }}, clk = $("{sid}-h-clk"), tv = $("{sid}-h-t"), merc = $("{sid}-h-merc");
    const draw = () => {{
      const mm = Math.round(st.m), hh = 6 + Math.floor(mm / 60);
      clk.textContent = String(hh).padStart(2, "0") + ":" + String(mm % 60).padStart(2, "0");
      tv.textContent = Math.round(st.t);
      const k = Math.min(1, Math.max(0.1, (st.t - 20) / 42)), h = 34 * k;
      merc.setAttribute("y", (52 - h).toFixed(1)); merc.setAttribute("height", h.toFixed(1));
      tv.parentNode.style.color = st.t >= 50 ? "#ff4636" : st.t >= 42 ? "#ff8a3a" : "#ffb547";
    }};
    draw();
    pop("#{sid}-h", 0.05);
{tw}
    tl.to("#{sid}-h", {{ opacity: 0, duration: 0.25, ease: "sine.in" }}, {ctx.dur - 0.3:.2f});"""
    return ctx.scene("", "", H.heat(f"{sid}-h", "06:00", "35"), js, bg="transparent", grain=0)
