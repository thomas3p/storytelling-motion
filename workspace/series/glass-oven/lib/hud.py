"""Overlays of 60°C รุ่งอรุณเดือด in the flood look: EP tag, cream knowledge card with a red number badge, number card with a
counting value and bar, chips, speech bubble, the heat chip (clock + temperature, top right), the big title and the end screen
(an elevator floor indicator + series line). KIT = "flat" makes tools/scenekit.py build these scenes with tools/flatkit.py.
All overlays start hidden; reveal them in scene JS with the kit helpers: cardIn("#id", t, hold), pop("#id", t, hold),
count($("id-num"), a, b, t, d, dec), ft("#id-bar", {scaleX: a}, {scaleX: b, ...}, t).
"""
KIT = "flat"

CSS = """
    .fk-ep { position: absolute; left: 48px; top: 176px; z-index: 19; display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 28px; color: #ffffff;
             background: rgba(8, 12, 22, 0.6); padding: 6px 20px 8px 8px; border-radius: 12px; opacity: 0; }
    .fk-ep b { background: #e5483a; padding: 0 12px 4px; border-radius: 8px; font-size: 28px; }
    .fk-card { position: absolute; left: 70px; top: 250px; width: 940px; z-index: 18; display: flex; align-items: center; gap: 28px; background: #fbf3dc; border-radius: 34px;
               padding: 26px 34px; box-shadow: 0 18px 44px rgba(0, 0, 0, 0.5), inset 0 -6px 0 rgba(0, 0, 0, 0.08); opacity: 0; }
    .fk-badge { position: absolute; left: -16px; top: -20px; width: 66px; height: 66px; border-radius: 50%; background: #e5483a; color: #ffffff; font-family: "Mitr", sans-serif;
                font-weight: 600; font-size: 36px; line-height: 1; display: flex; align-items: center; justify-content: center; border: 5px solid #fbf3dc; box-shadow: 0 4px 0 rgba(0, 0, 0, 0.25); }
    .fk-icon { flex: none; width: 168px; height: 168px; border-radius: 26px; background: #fde2c8; }
    .fk-icon svg { width: 168px; height: 168px; }
    .fk-tag { display: inline-block; font-weight: 700; font-size: 28px; color: #ffffff; background: #e5483a; padding: 0 14px 4px; border-radius: 8px; margin-bottom: 6px; }
    .fk-ct { font-weight: 700; font-size: 46px; line-height: 1.28; color: #1b2440; }
    .fk-cs { font-weight: 500; font-size: 30px; line-height: 1.4; color: #3f4e6c; margin-top: 4px; }
    .fk-sl { font-weight: 700; font-size: 34px; line-height: 1.3; color: #1b2440; }
    .fk-sv { font-family: "Mitr", sans-serif; font-weight: 600; font-size: 116px; line-height: 1.05; color: #d63a2c; }
    .fk-sv small { font-size: 46px; margin-left: 8px; }
    .fk-bar { width: 560px; height: 18px; border-radius: 9px; background: #e6dcc4; overflow: hidden; margin-top: 10px; }
    .fk-bar i { display: block; width: 100%; height: 100%; border-radius: 9px; background: #d63a2c; transform-origin: 0 50%; }
    .fk-chip { position: absolute; z-index: 18; display: flex; align-items: center; gap: 14px; background: #fbf3dc; border-radius: 22px; padding: 12px 24px 14px 12px;
               box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45); font-weight: 700; font-size: 38px; color: #1b2440; opacity: 0; }
    .fk-chip i { font-style: normal; width: 54px; height: 54px; border-radius: 50%; background: #e5483a; color: #fff; font-family: "Mitr", sans-serif; font-size: 30px; display: flex; align-items: center; justify-content: center; }
    .fk-bub { position: absolute; z-index: 18; background: #fbf3dc; color: #1b2440; border-radius: 30px; padding: 20px 30px 24px; font-weight: 700; font-size: 44px; line-height: 1.3; text-align: center;
              box-shadow: 0 14px 34px rgba(0, 0, 0, 0.5); opacity: 0; }
    .fk-bub::after { content: ""; position: absolute; bottom: -26px; width: 0; height: 0; border-left: 22px solid transparent; border-right: 22px solid transparent; border-top: 30px solid #fbf3dc; }
    .fk-bub.l::after { left: 60px; } .fk-bub.r::after { right: 60px; } .fk-bub.c::after { left: calc(50% - 22px); }
    .fk-src { position: absolute; left: 30px; right: 30px; top: 1168px; z-index: 18; text-align: center; font-weight: 500; font-size: 28px; color: #f2c89a; opacity: 0; white-space: nowrap; }
    .fk-heat { position: absolute; right: 48px; top: 168px; z-index: 19; display: flex; align-items: center; gap: 14px; background: rgba(8, 12, 22, 0.66); padding: 8px 22px 10px 12px;
               border-radius: 16px; font-family: "Mitr", sans-serif; font-weight: 600; color: #ffffff; opacity: 0; }
    .fk-heat svg { width: 40px; height: 64px; }
    .fk-heat .clk { font-size: 30px; color: #c9d4ea; }
    .fk-heat .tmp { font-size: 46px; line-height: 1; color: #ffb547; min-width: 128px; text-align: right; }
    .fk-title { position: absolute; left: 60px; right: 60px; top: 1430px; z-index: 19; text-align: center; opacity: 0; }
    .fk-title b { display: block; font-family: "Mitr", sans-serif; font-weight: 600; font-size: 150px; line-height: 1.0; color: #fff1c8; text-shadow: 0 6px 0 rgba(0, 0, 0, 0.35), 0 0 40px rgba(255, 90, 42, 0.9); }
    .fk-title u { display: block; text-decoration: none; font-weight: 700; font-size: 74px; line-height: 1.2; color: #ffffff; text-shadow: 0 4px 0 rgba(0, 0, 0, 0.35), 0 0 26px rgba(255, 90, 42, 0.7); }
    .fk-title span { display: block; margin-top: 16px; font-weight: 700; font-size: 40px; color: #ffffff; }
    .fk-title span em { font-style: normal; background: #e5483a; padding: 0 16px 6px; border-radius: 12px; }
    .fk-floor { position: absolute; left: 290px; top: 470px; width: 500px; z-index: 19; background: #1b1f28; border-radius: 34px; padding: 30px 0 34px; text-align: center;
                box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6), inset 0 0 0 8px #3a414e; opacity: 0; }
    .fk-floor-h { font-weight: 700; font-size: 34px; color: #c9d4ea; }
    .fk-floor-n { display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 8px; }
    .fk-floor-n svg { width: 70px; height: 90px; }
    .fk-floor-d { font-weight: 700; font-size: 36px; color: #ffb547; margin-top: 12px; }
    .fk-series { position: absolute; left: 60px; top: 1110px; width: 960px; z-index: 19; text-align: center; font-weight: 700; font-size: 46px; line-height: 1.4; color: #e9edf6; opacity: 0; }
    .fk-series span { display: block; font-weight: 500; font-size: 30px; color: #9aa6c0; }
    .fk-news { position: absolute; left: 0; right: 0; top: 1060px; z-index: 18; opacity: 0; }
    .fk-news b { display: inline-block; margin-left: 60px; background: #e5483a; color: #fff; font-weight: 700; font-size: 34px; padding: 4px 22px 8px; border-radius: 10px 10px 0 0; }
    .fk-news div { background: #fbf3dc; color: #1b2440; font-weight: 700; font-size: 44px; line-height: 1.3; padding: 16px 60px 20px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5); }"""

# icons for the cards (168 x 168 viewBox)
ICONS = {
    "car": '<circle cx="132" cy="38" r="20" fill="#ffb547" /><path d="M24,112 L34,84 Q40,70 56,70 L112,70 Q128,70 134,84 L144,112 Z" fill="#c8243a" /><rect x="18" y="104" width="132" height="30" rx="12" fill="#c8243a" />'
           '<path d="M50,82 L60,74 L108,74 L118,82 Z" fill="#9fd0ec" /><circle cx="48" cy="136" r="15" fill="#2a2a2e" /><circle cx="120" cy="136" r="15" fill="#2a2a2e" /><circle cx="48" cy="136" r="6" fill="#9a9aa0" /><circle cx="120" cy="136" r="6" fill="#9a9aa0" />',
    "thermo": '<rect x="70" y="20" width="28" height="100" rx="14" fill="#f2ead6" stroke="#3f4e6c" stroke-width="5" /><circle cx="84" cy="128" r="24" fill="#e5483a" stroke="#3f4e6c" stroke-width="5" /><rect x="78" y="56" width="12" height="76" rx="6" fill="#e5483a" />'
              '<path d="M104,40 L118,40 M104,62 L118,62 M104,84 L118,84" stroke="#3f4e6c" stroke-width="5" stroke-linecap="round" />',
    "sun": '<circle cx="84" cy="84" r="34" fill="#ffb547" />' + "".join(f'<rect x="80" y="18" width="8" height="22" rx="4" fill="#ffb547" transform="rotate({a} 84 84)" />' for a in range(0, 360, 45)),
}
THERMO_SVG = ('<svg viewBox="0 0 40 64"><rect x="13" y="3" width="14" height="44" rx="7" fill="#f2ead6" /><circle cx="20" cy="50" r="11" fill="#ff5a2a" />'
              '<rect id="{id}-merc" x="16.5" y="18" width="7" height="34" rx="3.5" fill="#ff5a2a" style="transform-origin: 20px 50px" /></svg>')


def ep_tag(id, ep, title):
    return f'    <div id="{id}" class="fk-ep"><b>EP{ep}</b>{title}</div>'


def card(id, n, icon, title, sub="", tag="", top=250):
    t = f'<div class="fk-tag">{tag}</div>' if tag else ""
    sh = f'<div class="fk-cs">{sub}</div>' if sub else ""
    return (f'    <div id="{id}" class="fk-card" style="top: {top}px"><div class="fk-badge">{n}</div><div class="fk-icon"><svg viewBox="0 0 168 168">{ICONS.get(icon, icon)}</svg></div>'
            f'<div>{t}<div class="fk-ct">{title}</div>{sh}</div></div>')


def stat(id, n, icon, label, value, unit, top=250, pct=0.0):
    return (f'    <div id="{id}" class="fk-card" style="top: {top}px"><div class="fk-badge">{n}</div><div class="fk-icon"><svg viewBox="0 0 168 168">{ICONS.get(icon, icon)}</svg></div>'
            f'<div><div class="fk-sl">{label}</div><div class="fk-sv"><span id="{id}-num">{value}</span><small>{unit}</small></div>'
            f'<div class="fk-bar"><i id="{id}-bar" style="transform: scaleX({pct})"></i></div></div></div>')


def chip(id, n, text, left, top):
    return f'    <div id="{id}" class="fk-chip" style="left: {left}px; top: {top}px"><i>{n}</i>{text}</div>'


def bubble(id, text, left, top, width, tail="l"):
    return f'    <div id="{id}" class="fk-bub {tail}" style="left: {left}px; top: {top}px; width: {width}px">{text}</div>'


def src(id, text, top=1168):
    return f'    <div id="{id}" class="fk-src" style="top: {top}px">{text}</div>'


def heat(id, clock, temp):
    """Clock + temperature chip, top right. Animate the numbers with count() on {id}-t (°C) and set {id}-clk text."""
    return (f'    <div id="{id}" class="fk-heat">{THERMO_SVG.format(id=id)}<div><div class="clk" id="{id}-clk">{clock}</div>'
            f'<div class="tmp"><span id="{id}-t">{temp}</span>°C</div></div></div>')


def news(id, head, text):
    return f'    <div id="{id}" class="fk-news"><b>{head}</b><div>{text}</div></div>'


def title(id, big, sub, ep, name):
    return f'    <div id="{id}" class="fk-title"><b>{big}</b><u>{sub}</u><span><em>EP{ep}</em> {name}</span></div>'


def floor_card(id, head, digits_svg, sub):
    """End screen: an elevator floor indicator. digits_svg is SVG markup (led() from the kit) placed beside a down arrow."""
    return (f'    <div id="{id}" class="fk-floor"><div class="fk-floor-h">{head}</div><div class="fk-floor-n"><svg viewBox="0 0 70 90"><path d="M35,84 L6,46 L24,46 L24,6 L46,6 L46,46 L64,46 Z" fill="#ff4636" /></svg>'
            f'<svg id="{id}-led" viewBox="0 0 200 130" style="width: 200px; height: 130px">{digits_svg}</svg></div><div class="fk-floor-d">{sub}</div></div>')


def series_line(id, title, sub):
    return f'    <div id="{id}" class="fk-series">{title}<span>{sub}</span></div>'
