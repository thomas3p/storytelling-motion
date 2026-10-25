"""Game-style pop-up HUD for the channel (the default HUD from 2026-10-24).

The user's rule: on-screen HUD = update pop-ups like in a game (quest updated, new clue, item received, status changed),
sliding in, holding, and sliding out. NOT a framed screen with corner brackets. Corner frames / REC lines are only for a
series whose look is a camera view (e.g. แทรกซึม = CCTV).

Use from a series lib hud.py:   import hudpop;  CSS += hudpop.CSS;  JS += hudpop.JS;  pop = hudpop.pop  ...
All elements start hidden; scenes reveal them with the JS helpers (timeline driven, no CSS animation).

  pop(id, label, text, kind="update", icon=None, top=170, side="right")   one pop-up card
  stat(id, label, value, pct, kind="warn", top=170, side="left")         a status card with a bar ({id}-bar)
  objective(id, label, text, top=150)                                    a quest tracker line with a checkbox ({id}-chk)
  toast(id, text, kind="item", top=980)                                  a small centred "+1" style toast

JS helpers (inside the scene timeline):
  popIn(sel, t, hold = 2.4, side = "right")   slide in with a shine sweep; slides out after `hold` s (hold 0 = stays)
  popOut(sel, t, side = "right")
  statTo(sel, t, pct, d = 0.6)                 grow/shrink a stat bar to pct (0-100)
  tick(sel, t)                                 tick an objective checkbox
Kinds: update (cyan), quest (gold), clue (purple), warn (red), item (green). Keep text >= 28 px and hold >= 0.5 s + 0.3 s/word.
Stack several pop-ups at top = 170, 300, 430 … (they never sit in the caption band, y 1140-1300).
"""

KINDS = {"update": ("#4fc3ff", "↻"), "quest": ("#ffc94a", "★"), "clue": ("#b18cff", "?"), "warn": ("#ff4d5e", "!"), "item": ("#7dffb0", "+")}

CSS = """
    .pop { position: absolute; width: 620px; display: flex; align-items: center; gap: 20px; padding: 16px 22px 18px 16px; border-radius: 20px;
           background: rgba(10,14,24,0.9); border: 2px solid var(--pc); box-shadow: 0 0 28px rgba(0,0,0,0.45), 0 0 18px var(--pg); overflow: hidden; opacity: 0; }
    .pop.r { right: 36px; } .pop.l { left: 36px; }
    .pop-ic { flex: none; width: 78px; height: 78px; border-radius: 18px; background: var(--pc); color: #0a0e18; font-size: 50px; font-weight: 800; line-height: 78px; text-align: center; }
    .pop-tx { flex: 1; min-width: 0; }
    .pop-lb { font-size: 28px; font-weight: 700; color: var(--pc); letter-spacing: 1px; line-height: 1.2; }
    .pop-t { font-size: 38px; font-weight: 800; color: #ffffff; line-height: 1.18; }
    .pop-sh { position: absolute; top: 0; bottom: 0; left: 0; width: 120px; background: linear-gradient(100deg, transparent, rgba(255,255,255,0.28), transparent); opacity: 0; }
    .pop-bar { margin-top: 10px; height: 16px; border-radius: 8px; background: rgba(255,255,255,0.14); overflow: hidden; }
    .pop-bar i { display: block; height: 100%; width: 0%; background: var(--pc); border-radius: 8px; }
    .obj { position: absolute; left: 36px; display: flex; align-items: center; gap: 16px; padding: 12px 22px 14px 14px; border-radius: 14px; background: rgba(10,14,24,0.82); border-left: 6px solid #ffc94a; opacity: 0; }
    .obj-chk { flex: none; width: 40px; height: 40px; border-radius: 8px; border: 4px solid #ffc94a; color: #0a0e18; font-size: 30px; font-weight: 800; line-height: 32px; text-align: center; }
    .obj-lb { font-size: 28px; font-weight: 700; color: #ffc94a; } .obj-t { font-size: 34px; font-weight: 800; color: #ffffff; }
    .tst { position: absolute; left: 0; right: 0; margin: 0 auto; width: fit-content; padding: 12px 34px 16px; border-radius: 999px; background: rgba(10,14,24,0.88); border: 3px solid var(--pc); color: var(--pc); font-size: 40px; font-weight: 800; opacity: 0; }"""


def _vars(kind):
    c, _ = KINDS.get(kind, KINDS["update"])
    return f"--pc: {c}; --pg: {c}55;"


def pop(id, label, text, kind="update", icon=None, top=170, side="right"):
    c, ic = KINDS.get(kind, KINDS["update"])
    return (f'    <div id="{id}" class="pop {"r" if side == "right" else "l"}" style="top: {top}px; {_vars(kind)}">'
            f'<div class="pop-ic">{icon or ic}</div><div class="pop-tx"><div class="pop-lb">{label}</div><div class="pop-t">{text}</div></div><span class="pop-sh"></span></div>')


def stat(id, label, value, pct=0, kind="warn", top=170, side="left"):
    c, ic = KINDS.get(kind, KINDS["warn"])
    return (f'    <div id="{id}" class="pop {"r" if side == "right" else "l"}" style="top: {top}px; {_vars(kind)}">'
            f'<div class="pop-ic">{ic}</div><div class="pop-tx"><div class="pop-lb">{label}</div><div class="pop-t">{value}</div>'
            f'<div class="pop-bar"><i id="{id}-bar" style="width: {pct}%;"></i></div></div><span class="pop-sh"></span></div>')


def objective(id, label, text, top=150):
    return (f'    <div id="{id}" class="obj" style="top: {top}px;"><div id="{id}-chk" class="obj-chk"><span id="{id}-v" style="opacity: 0;">✓</span></div>'
            f'<div><div class="obj-lb">{label}</div><div class="obj-t">{text}</div></div></div>')


def toast(id, text, kind="item", top=980):
    return f'    <div id="{id}" class="tst" style="top: {top}px; {_vars(kind)}">{text}</div>'


JS = """
    // game-style pop-ups: slide in with a shine sweep, hold, slide out
    function popIn(sel, t, hold = 2.4, side = "right") {
      const dx = side === "right" ? 160 : -160;
      tl.fromTo(sel, { opacity: 0, x: dx, scale: 0.96 }, { opacity: 1, x: 0, scale: 1, duration: 0.38, ease: "back.out(1.7)", immediateRender: false }, t);
      tl.fromTo(sel + " .pop-ic", { scale: 1.35 }, { scale: 1, duration: 0.35, ease: "back.out(2.4)", immediateRender: false }, t + 0.12);
      tl.fromTo(sel + " .pop-sh", { opacity: 1, x: -140 }, { opacity: 1, x: 760, duration: 0.6, ease: "power2.inOut", immediateRender: false }, t + 0.2);
      if (hold > 0) tl.to(sel, { opacity: 0, x: dx, duration: 0.3, ease: "power2.in" }, t + 0.38 + hold);
    }
    function popOut(sel, t, side = "right") { tl.to(sel, { opacity: 0, x: side === "right" ? 160 : -160, duration: 0.3, ease: "power2.in" }, t); }
    function statTo(sel, t, pct, d = 0.6) { tl.to(sel, { width: pct + "%", duration: d, ease: "power2.out" }, t); }
    function tick(sel, t) { tl.set(sel + "-v", { opacity: 1 }, t); tl.fromTo(sel + "-chk", { scale: 1.4, backgroundColor: "#ffc94a" }, { scale: 1, backgroundColor: "#ffc94a", duration: 0.3, ease: "back.out(2)", immediateRender: false }, t); }
    function toastIn(sel, t, hold = 1.6) { tl.fromTo(sel, { opacity: 0, y: 30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, t); tl.to(sel, { opacity: 0, y: -30, duration: 0.3 }, t + 0.3 + hold); }"""
