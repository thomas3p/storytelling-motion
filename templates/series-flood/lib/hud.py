"""Overlays of ปอบยุค 5G in the flood look (survival-5styles): EP tag, cream knowledge card with a red number badge, number card
with a counting value and bar, small chips, speech bubble, receipt, and the end screen (appointment card + series line).
KIT = "flat" makes tools/scenekit.py build these scenes with tools/flatkit.py.
All overlays start hidden; reveal them in scene JS with the kit helpers: cardIn("#id", t, hold), pop("#id", t, hold),
count($("id-num"), a, b, t, d, dec), ft("#id-bar", {scaleX: a}, {scaleX: b, ...}, t).
"""
KIT = "flat"

CSS = """
    .fk-ep { position: absolute; left: 48px; top: 176px; z-index: 19; display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 28px; color: #ffffff;
             background: rgba(8, 12, 22, 0.6); padding: 6px 20px 8px 8px; border-radius: 12px; opacity: 0; }
    .fk-ep b { background: #e5483a; padding: 0 12px 4px; border-radius: 8px; font-size: 28px; }
    .fk-card { position: absolute; left: 70px; top: 230px; width: 940px; z-index: 18; display: flex; align-items: center; gap: 28px; background: #fbf3dc; border-radius: 34px;
               padding: 26px 34px; box-shadow: 0 18px 44px rgba(0, 0, 0, 0.5), inset 0 -6px 0 rgba(0, 0, 0, 0.08); opacity: 0; }
    .fk-badge { position: absolute; left: -16px; top: -20px; width: 66px; height: 66px; border-radius: 50%; background: #e5483a; color: #ffffff; font-family: "Mitr", sans-serif;
                font-weight: 600; font-size: 36px; line-height: 1; display: flex; align-items: center; justify-content: center; border: 5px solid #fbf3dc; box-shadow: 0 4px 0 rgba(0, 0, 0, 0.25); }
    .fk-icon { flex: none; width: 168px; height: 168px; border-radius: 26px; background: #f6dcdc; }
    .fk-icon svg { width: 168px; height: 168px; }
    .fk-tag { display: inline-block; font-weight: 700; font-size: 28px; color: #ffffff; background: #e5483a; padding: 0 14px 4px; border-radius: 8px; margin-bottom: 6px; }
    .fk-ct { font-weight: 700; font-size: 48px; line-height: 1.28; color: #1b2440; }
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
    .fk-rcpt { position: absolute; z-index: 18; width: 420px; background: #ffffff; color: #1b2440; padding: 22px 30px 30px; font-weight: 500; font-size: 30px; line-height: 1.5;
               box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5); opacity: 0; clip-path: polygon(0 0, 100% 0, 100% 96%, 92% 100%, 84% 96%, 76% 100%, 68% 96%, 60% 100%, 52% 96%, 44% 100%, 36% 96%, 28% 100%, 20% 96%, 12% 100%, 4% 96%, 0 100%); }
    .fk-rcpt b { display: block; font-weight: 700; font-size: 34px; text-align: center; border-bottom: 3px dashed #c9cdd2; padding-bottom: 8px; margin-bottom: 8px; }
    .fk-rcpt em { display: block; font-style: normal; font-family: "Mitr", sans-serif; font-weight: 600; font-size: 54px; color: #d63a2c; text-align: right; }
    .fk-paid { position: relative; display: table; margin: 10px auto 0; transform: rotate(-8deg); border: 6px solid #2e9e5a; color: #2e9e5a; font-weight: 700; font-size: 40px; padding: 0 16px 4px; border-radius: 12px; }
    .fk-appt { position: absolute; left: 330px; top: 560px; width: 420px; z-index: 19; background: #fbf3dc; border-radius: 30px; text-align: center; box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6); opacity: 0; }
    .fk-appt-h { background: #e5483a; color: #ffffff; font-weight: 700; font-size: 34px; line-height: 1.3; padding: 22px 0 18px; border-radius: 30px 30px 0 0; position: relative; }
    .fk-appt-h::before, .fk-appt-h::after { content: ""; position: absolute; top: -18px; width: 16px; height: 40px; border-radius: 8px; background: #2a2f3c; }
    .fk-appt-h::before { left: 110px; } .fk-appt-h::after { right: 110px; }
    .fk-appt-d { font-weight: 700; font-size: 44px; line-height: 1.3; color: #1b2440; margin-top: 18px; }
    .fk-appt-n { font-family: "Mitr", sans-serif; font-weight: 600; font-size: 230px; line-height: 1.05; color: #e5483a; padding-bottom: 26px; }
    .fk-series { position: absolute; left: 60px; top: 1110px; width: 960px; z-index: 19; text-align: center; font-weight: 700; font-size: 46px; line-height: 1.4; color: #e9edf6; opacity: 0; }
    .fk-series span { display: block; font-weight: 500; font-size: 30px; color: #9aa6c0; }
    .fk-title { position: absolute; left: 70px; right: 70px; top: 1440px; z-index: 19; text-align: center; opacity: 0; }
    .fk-title b { display: inline-block; font-weight: 700; font-size: 96px; line-height: 1.1; color: #ffffff; text-shadow: 0 6px 0 rgba(0, 0, 0, 0.35), 0 0 30px rgba(255, 61, 127, 0.6); }
    .fk-title span { display: block; margin-top: 10px; font-weight: 700; font-size: 40px; color: #ffffff; }
    .fk-title span em { font-style: normal; background: #e5483a; padding: 0 16px 6px; border-radius: 12px; }"""

# icons for the cards (168 x 168 viewBox)
ICONS = {
    "lipo": '<rect x="54" y="36" width="60" height="104" rx="14" fill="#f2ead6" stroke="#3f4e6c" stroke-width="5" /><rect x="58" y="78" width="52" height="58" rx="10" fill="#f2d27a" /><rect x="66" y="22" width="36" height="16" rx="5" fill="#3f4e6c" /><path d="M114,60 L132,60 M114,84 L132,84 M114,108 L132,108" stroke="#3f4e6c" stroke-width="4" />',
    "bed": '<rect x="24" y="92" width="120" height="30" rx="8" fill="#3f4e6c" /><rect x="24" y="70" width="44" height="26" rx="10" fill="#f2ead6" stroke="#3f4e6c" stroke-width="4" /><path d="M28,122 L28,142 M140,122 L140,142" stroke="#3f4e6c" stroke-width="7" stroke-linecap="round" /><circle cx="120" cy="50" r="22" fill="#fbf3dc" stroke="#e5483a" stroke-width="5" /><path d="M120,38 L120,52 L130,58" stroke="#e5483a" stroke-width="5" fill="none" stroke-linecap="round" />',
    "bin": '<path d="M46,140 L52,58 L116,58 L122,140 Z" fill="#c8243a" /><path d="M40,58 L42,44 Q84,36 126,44 L128,58 Z" fill="#a81c30" /><circle cx="84" cy="98" r="16" fill="none" stroke="#ffe9e9" stroke-width="5" /><circle cx="84" cy="98" r="5" fill="#ffe9e9" />',
    "drop": '<path d="M84,24 Q120,74 120,100 A36,36 0 0 1 48,100 Q48,74 84,24 Z" fill="#c8243a" /><path d="M66,100 A18,18 0 0 0 84,118" stroke="#ff9aa4" stroke-width="6" fill="none" stroke-linecap="round" />',
    "nurse": '<circle cx="84" cy="70" r="30" fill="#eab48e" /><path d="M54,58 L114,58 L108,36 Q84,28 60,36 Z" fill="#ffffff" stroke="#3f4e6c" stroke-width="3" /><rect x="78" y="40" width="12" height="12" fill="#e5483a" /><path d="M40,146 Q44,104 84,104 Q124,104 128,146 Z" fill="#f4f7fb" stroke="#3f4e6c" stroke-width="3" />',
    "book": '<rect x="38" y="30" width="92" height="114" rx="8" fill="#f2ead6" stroke="#3f4e6c" stroke-width="5" /><path d="M54,58 L114,58 M54,78 L114,78 M54,98 L96,98" stroke="#3f4e6c" stroke-width="5" stroke-linecap="round" /><text x="84" y="132" text-anchor="middle" font-family="Mitr" font-weight="600" font-size="30" fill="#e5483a">12 กก.</text>',
}


def ep_tag(id, ep, title):
    return f'    <div id="{id}" class="fk-ep"><b>EP{ep}</b>{title}</div>'


def card(id, n, icon, title, sub="", tag="", top=230):
    t = f'<div class="fk-tag">{tag}</div>' if tag else ""
    sh = f'<div class="fk-cs">{sub}</div>' if sub else ""
    return (f'    <div id="{id}" class="fk-card" style="top: {top}px"><div class="fk-badge">{n}</div><div class="fk-icon"><svg viewBox="0 0 168 168">{ICONS.get(icon, icon)}</svg></div>'
            f'<div>{t}<div class="fk-ct">{title}</div>{sh}</div></div>')


def stat(id, n, icon, label, value, unit, top=230, pct=0.0):
    return (f'    <div id="{id}" class="fk-card" style="top: {top}px"><div class="fk-badge">{n}</div><div class="fk-icon"><svg viewBox="0 0 168 168">{ICONS.get(icon, icon)}</svg></div>'
            f'<div><div class="fk-sl">{label}</div><div class="fk-sv"><span id="{id}-num">{value}</span><small>{unit}</small></div>'
            f'<div class="fk-bar"><i id="{id}-bar" style="transform: scaleX({pct})"></i></div></div></div>')


def chip(id, n, text, left, top):
    return f'    <div id="{id}" class="fk-chip" style="left: {left}px; top: {top}px"><i>{n}</i>{text}</div>'


def bubble(id, text, left, top, width, tail="l"):
    return f'    <div id="{id}" class="fk-bub {tail}" style="left: {left}px; top: {top}px; width: {width}px">{text}</div>'


def receipt(id, left, top, lines, total):
    rows = "".join(f'<div>{a}<span style="float: right">{b}</span></div>' for a, b in lines)
    return f'    <div id="{id}" class="fk-rcpt" style="left: {left}px; top: {top}px"><b>คลินิกหมอพิม</b>{rows}<em>{total}</em><div class="fk-paid">ชำระแล้ว</div></div>'


def appt(id, head, line, num):
    return f'    <div id="{id}" class="fk-appt"><div class="fk-appt-h">{head}</div><div class="fk-appt-d">{line}</div><div class="fk-appt-n">{num}</div></div>'


def series_line(id, title, sub):
    return f'    <div id="{id}" class="fk-series">{title}<span>{sub}</span></div>'


def title(id, big, ep, name):
    return f'    <div id="{id}" class="fk-title"><b>{big}</b><span><em>EP{ep}</em> {name}</span></div>'
