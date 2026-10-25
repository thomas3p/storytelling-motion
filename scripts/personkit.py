"""Flat-vector character kit for HyperFrames (the look the user picked: Thai guy, grey hoodie,
navy jeans, white sneakers, black side-fringe hair, peach skin; no outlines).

scene(sid, dur, css, svg, overlays, js, bg="#0b0d14") -> scene HTML
- svg is the drawing (backgrounds, props, and <g id="..."></g> slots for characters).
- js creates characters with PERSON.fig("#slot", {keys:[...], look:{...}}) and must define FIGS.
  keys: {t, p, x, y, s, dir, d, move, anchor, mood, rot, rate, prop:"phone", glow:true}; look adds hair "neat" and glasses:true; p = pose name, "walk"/"run" cycle or 10 numbers.
  moods: "", "smile", "worried", "scared", "closed", "talk" (mouth flaps), "sad".
  look: {hair:"fringe"|"bun"|"long", lip, lash, hairCol, skin, top, topDark, topLight, pants, pantsLight, shoe}
- DUST(selector, n, seed, box) adds floating dust motes redrawn from timeline time.
"""

RIG = r"""
const PERSON = (() => {
  const P = {
    stand: [0, 0, -10, 10, 10, -8, -6, 0, 6, 0],
    idle: [2, 4, -8, 12, 8, 14, -6, 0, 6, 0],
    walkA: [4, 0, -26, 20, 28, 25, -22, -18, 24, -4],
    walkB: [4, 0, 28, 25, -26, 20, 24, -4, -22, -18],
    runA: [14, 0, -50, 70, 60, 80, -35, -60, 45, -20],
    runB: [14, 0, 60, 80, -50, 70, 45, -20, -35, -60],
    phone: [6, 16, 40, 88, 46, 80, -6, 0, 6, 0],
    ear: [0, -4, -10, 8, 112, 98, -6, 0, 6, 0],
    point: [0, 0, -10, 10, 92, 0, -6, 0, 6, 0],
    reach: [10, 4, -10, 10, 70, 12, -8, 0, 10, 0],
    scared: [-10, -10, 150, 20, 155, 15, -16, 0, 16, 0],
    flinch: [-8, -14, 40, 120, 50, 115, -12, 0, 12, 0],
    cover: [30, 25, 140, 110, 145, 105, 40, -110, 50, -120],
    crouch: [34, 20, 55, 10, 68, 10, 55, -110, 62, -115],
    kneel: [22, 18, 55, 25, 62, 18, 0, -92, 70, -78],
    hide: [55, 35, 150, 100, 70, 20, 65, -130, 75, -135],
    sit: [0, 2, -5, 40, 25, 60, 82, -84, 88, -88],
    sitwork: [8, 10, 50, 60, 58, 54, 82, -84, 88, -88],
    think: [0, 8, -10, 10, 22, 140, -6, 0, 6, 0],
    whisper: [16, 10, -10, 10, 30, 135, -10, 0, 12, 0],
    sigh: [-4, -6, -4, 4, 4, -2, -6, 0, 6, 0],
    knock: [8, 0, -10, 10, 72, 75, -6, 0, 8, 0],
    back: [-14, -8, 60, 40, 75, 30, -22, 0, 18, 0],
    look: [-6, -22, -10, 10, 10, -8, -6, 0, 6, 0],
    wave: [0, 0, -10, 10, 150, 30, -6, 0, 6, 0],
    hold: [4, 6, 45, 60, 50, 55, -6, 0, 6, 0],
    stretch: [0, -14, 165, 8, 170, 6, -6, 0, 6, 0],
    tiptoe: [10, 6, 40, 60, 30, 70, -16, -12, 16, -12],
    peek: [18, 10, -10, 10, 40, 60, -10, 0, 12, 0],
    drive: [6, 8, 62, 34, 70, 26, 82, -84, 88, -88],
    drivelook: [-4, -24, 62, 34, 70, 26, 82, -84, 88, -88],
  };
  const R = Math.PI / 180;
  const ez = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2);
  const CYC = { walk: ["walkA", "walkB", 1.8], run: ["runA", "runB", 3.2] };
  function poseOf(k, t) {
    if (Array.isArray(k.p)) return k.p;
    const c = CYC[k.p];
    if (!c) return P[k.p];
    const ph = (Math.sin(t * (k.rate || c[2]) * Math.PI) + 1) / 2;
    return P[c[0]].map((v, i) => v + (P[c[1]][i] - v) * ph);
  }
  function norm(keys) {
    const out = [];
    let prev = { x: 0, y: 0, s: 1, dir: 1, anchor: "feet", mood: "", rot: 0 };
    for (const k of keys) { const n = Object.assign({}, prev, k); n.d = k.d === undefined ? 0.3 : k.d; n.move = !!k.move; out.push(n); prev = n; }
    return out;
  }
  function state(K, t) {
    let i = 0;
    while (i + 1 < K.length && K[i + 1].t <= t) i++;
    const a = K[i], b = K[i + 1];
    if (t < a.t || !b) return { k: a, p: poseOf(a, t), x: a.x, y: a.y, s: a.s, rot: a.rot };
    const u = ez((t - (b.t - b.d)) / b.d);
    const pa = poseOf(a, t), pb = poseOf(b, t);
    let w = u;
    if (b.move) w = Math.min(1, Math.max(0, (t - a.t) / (b.t - a.t)));
    return { k: u > 0.5 ? b : a, p: pa.map((v, j) => v + (pb[j] - v) * u), x: a.x + (b.x - a.x) * w, y: a.y + (b.y - a.y) * w, s: a.s + (b.s - a.s) * u, rot: a.rot + (b.rot - a.rot) * u };
  }
  const LOOK = { hair: "fringe", hairCol: "#15151c", skin: "#f2c09b", skinDark: "#e0a882", top: "#8792a3", topDark: "#6c7686", topLight: "#9ea9b9", pants: "#27304a", pantsLight: "#323d5c", shoe: "#f4f4f2" };
  function fig(sel, cfg) {
    const L = Object.assign({}, LOOK, cfg.look || {});
    const g = document.querySelector(sel), ns = "http://www.w3.org/2000/svg";
    const mk = (tag, attrs) => { const e = document.createElementNS(ns, tag); for (const a in attrs) e.setAttribute(a, attrs[a]); g.appendChild(e); return e; };
    const limb = (col, w) => mk("path", { fill: "none", stroke: col, "stroke-width": w, "stroke-linecap": "round", "stroke-linejoin": "round" });
    const f = { g, L, K: norm(cfg.keys), shadow: mk("ellipse", { fill: "#000", opacity: 0.25 }) };
    f.legB = limb(L.pants, 27); f.shoeB = mk("path", { fill: L.shoe });
    f.armB = limb(L.topDark, 23); f.handB = mk("circle", { r: 12, fill: L.skinDark });
    f.torso = limb(L.top, 60); f.pocket = limb(L.topDark, 13);
    f.legF = limb(L.pantsLight, 27); f.shoeF = mk("path", { fill: L.shoe });
    f.hairBack = mk("path", { fill: L.hairCol }); f.neck = limb(L.skinDark, 16); f.head = mk("circle", { r: 40, fill: L.skin }); f.ear = mk("circle", { r: 9, fill: L.skinDark });
    f.hair = mk("path", { fill: L.hairCol }); f.bun = mk("circle", { r: L.hair === "bun" ? 19 : 0, fill: L.hairCol });
    f.brow = mk("path", { fill: "none", stroke: L.hairCol, "stroke-width": 5.5, "stroke-linecap": "round" });
    f.eye = mk("circle", { fill: "#1a1a1f" }); f.eyeHi = mk("circle", { r: 1.6, fill: "#fff" });
    f.mouth = mk("path", { fill: "none", stroke: L.lip || "#7a3b2e", "stroke-width": 4.5, "stroke-linecap": "round" });
    f.lash = mk("path", { fill: "none", stroke: L.hairCol, "stroke-width": 3.5, "stroke-linecap": "round" });
    f.lens = mk("circle", { r: L.glasses ? 13 : 0, fill: "#dfe9f5", "fill-opacity": 0.18, stroke: "#1d1f26", "stroke-width": 4 });
    f.gframe = mk("path", { fill: "none", stroke: "#1d1f26", "stroke-width": 4, "stroke-linecap": "round" });
    f.armF = limb(L.topLight, 23); f.handF = mk("circle", { r: 12, fill: L.skin });
    f.prop = mk("rect", { width: 0, height: 0, rx: 6, fill: "#15171f", stroke: "#3a4256", "stroke-width": 3 });
    f.glow = mk("circle", { r: 0, fill: "#a0c4ff", opacity: 0.25 });
    return f;
  }
  const P2 = (z) => z[0].toFixed(1) + " " + z[1].toFixed(1);
  function draw(f, t) {
    const st = state(f.K, t), k = st.k, dir = k.dir, L = f.L;
    let [lean, tilt, aB, eB, aF, eF, hB, kB, hF, kF] = st.p;
    // idle breath: a slow 1.5 degree rock of the torso so a held pose is alive
    lean += Math.sin(t * 2.1) * 1.2;
    const v = (len, ang) => [Math.sin(ang * R) * len * dir, Math.cos(ang * R) * len];
    const add = (a, b) => [a[0] + b[0], a[1] + b[1]];
    const H = [0, 0];
    const S = [Math.sin(lean * R) * 90 * dir, -Math.cos(lean * R) * 90];
    const N = add(S, [Math.sin((lean + tilt * 0.5) * R) * 30 * dir, -Math.cos((lean + tilt * 0.5) * R) * 30]);
    const C = add(S, [Math.sin((lean + tilt) * R) * 66 * dir, -Math.cos((lean + tilt) * R) * 66]);
    const kb = add(H, v(76, hB)), fb = add(kb, v(74, hB + kB));
    const kf = add(H, v(76, hF)), ff = add(kf, v(74, hF + kF));
    const eb = add(S, v(66, aB)), wb = add(eb, v(64, aB + eB));
    const ef = add(S, v(66, aF)), wf = add(ef, v(64, aF + eF));
    const lift = k.anchor === "hip" ? 0 : -Math.max(fb[1], ff[1]) - 12;
    const up = (z) => [z[0], z[1] + lift];
    const [h, s2, n2, c] = [up(H), up(S), up(N), up(C)];
    const shoe = (foot) => { const q = up(foot); return `M${(q[0] - 18 * dir).toFixed(1)} ${(q[1] + 14).toFixed(1)} l0 -14 q${dir * 2} -10 ${dir * 16} -10 q${dir * 10} 2 ${dir * 16} 8 l${dir * 18} 6 q${dir * 10} 4 ${dir * 8} 10 z`; };
    f.legB.setAttribute("d", `M${P2(h)} L${P2(up(kb))} L${P2(up(fb))}`);
    f.legF.setAttribute("d", `M${P2(h)} L${P2(up(kf))} L${P2(up(ff))}`);
    f.shoeB.setAttribute("d", shoe(fb)); f.shoeF.setAttribute("d", shoe(ff));
    // torso as a rounded capsule from the hip to just under the shoulder
    const tb = [h[0] + (s2[0] - h[0]) * 0.12, h[1] + (s2[1] - h[1]) * 0.12], tt = [h[0] + (s2[0] - h[0]) * 0.86, h[1] + (s2[1] - h[1]) * 0.86];
    f.torso.setAttribute("d", `M${P2(tb)} L${P2(tt)}`);
    const pk = [h[0] + (s2[0] - h[0]) * 0.3 + 10 * dir, h[1] + (s2[1] - h[1]) * 0.3];
    f.pocket.setAttribute("d", `M${P2(pk)} l${dir * 12} 0`);
    f.armB.setAttribute("d", `M${P2(s2)} L${P2(up(eb))} L${P2(up(wb))}`);
    f.armF.setAttribute("d", `M${P2(s2)} L${P2(up(ef))} L${P2(up(wf))}`);
    const hb = up(wb), hf = up(wf);
    f.handB.setAttribute("cx", hb[0].toFixed(1)); f.handB.setAttribute("cy", hb[1].toFixed(1));
    f.handF.setAttribute("cx", hf[0].toFixed(1)); f.handF.setAttribute("cy", hf[1].toFixed(1));
    f.neck.setAttribute("d", `M${P2(s2)} L${P2(n2)}`);
    f.head.setAttribute("cx", c[0].toFixed(1)); f.head.setAttribute("cy", c[1].toFixed(1));
    f.ear.setAttribute("cx", (c[0] - 18 * dir).toFixed(1)); f.ear.setAttribute("cy", (c[1] + 8).toFixed(1));
    const FS = 40 / 31, X = (dx) => (c[0] + dx * FS * dir).toFixed(1), Y = (dy) => (c[1] + dy * FS).toFixed(1);
    // long hair: a back sheet behind the head that falls to the shoulder blades
    f.hairBack.setAttribute("d", L.hair === "long" ? `M${X(-33)} ${Y(-10)} C${X(-40)} ${Y(-44)} ${X(4)} ${Y(-54)} ${X(22)} ${Y(-36)} C${X(16)} ${Y(-14)} ${X(2)} ${Y(20)} ${X(-2)} ${Y(56)} C${X(-12)} ${Y(64)} ${X(-28)} ${Y(64)} ${X(-38)} ${Y(56)} C${X(-44)} ${Y(30)} ${X(-42)} ${Y(8)} ${X(-33)} ${Y(-10)} Z` : "");
    if (L.hair === "bun") {
      f.hair.setAttribute("d", `M${X(-32)} ${Y(4)} C${X(-34)} ${Y(-30)} ${X(-10)} ${Y(-40)} ${X(10)} ${Y(-36)} C${X(26)} ${Y(-32)} ${X(32)} ${Y(-20)} ${X(30)} ${Y(-12)} C${X(14)} ${Y(-22)} ${X(-8)} ${Y(-18)} ${X(-16)} ${Y(8)} Z`);
      f.bun.setAttribute("cx", X(-24)); f.bun.setAttribute("cy", Y(-30));
    } else if (L.hair === "neat") {
      // short and side-parted, the hairline sits high so the forehead shows
      f.hair.setAttribute("d", `M${X(-33)} ${Y(6)} C${X(-38)} ${Y(-30)} ${X(-8)} ${Y(-47)} ${X(16)} ${Y(-41)} C${X(32)} ${Y(-37)} ${X(40)} ${Y(-24)} ${X(37)} ${Y(-14)} C${X(24)} ${Y(-25)} ${X(6)} ${Y(-29)} ${X(-8)} ${Y(-27)} C${X(-18)} ${Y(-23)} ${X(-22)} ${Y(-8)} ${X(-21)} ${Y(8)} Z`);
    } else {
      f.hair.setAttribute("d", `M${X(-33)} ${Y(8)} C${X(-38)} ${Y(-30)} ${X(-8)} ${Y(-46)} ${X(16)} ${Y(-38)} C${X(36)} ${Y(-32)} ${X(41)} ${Y(-14)} ${X(36)} ${Y(-1)} C${X(28)} ${Y(-15)} ${X(12)} ${Y(-21)} ${X(-2)} ${Y(-15)} C${X(-12)} ${Y(-9)} ${X(-17)} ${Y(-1)} ${X(-19)} ${Y(10)} Z`);
    }
    const m = k.mood, big = m === "scared";
    f.eye.setAttribute("r", m === "closed" ? 0 : big ? 7.5 : 5.6);
    f.eye.setAttribute("cx", X(16)); f.eye.setAttribute("cy", Y(-2));
    f.eyeHi.setAttribute("r", m === "closed" ? 0 : 2);
    f.eyeHi.setAttribute("cx", X(17.6)); f.eyeHi.setAttribute("cy", Y(-3.4));
    const browY = big ? -16 : m === "worried" || m === "sad" ? -12 : -11;
    const browTilt = m === "worried" || m === "sad" ? -5 : big ? -2 : 1;
    f.brow.setAttribute("d", `M${X(9)} ${Y(browY)} l${dir * 18} ${browTilt * 1.3}`);
    let mo;
    if (m === "scared") mo = `M${X(16)} ${Y(14)} m-4 0 a4 5 0 1 0 8 0 a4 5 0 1 0 -8 0`;
    else if (m === "smile") mo = `M${X(9)} ${Y(12)} q${dir * 7} 6 ${dir * 14} 0`;
    else if (m === "worried" || m === "sad") mo = `M${X(10)} ${Y(16)} q${dir * 6} -4 ${dir * 12} 0`;
    else if (m === "talk") { const o = (Math.floor(t * 9) % 3) * 2.5; mo = `M${X(10)} ${Y(13)} q${dir * 6} ${(3 + o).toFixed(1)} ${dir * 12} 0`; }
    else if (m === "closed") mo = `M${X(10)} ${Y(14)} l${dir * 10} 0`;
    else mo = `M${X(10)} ${Y(13)} q${dir * 6} 3 ${dir * 12} 0`;
    if (m === "closed") f.brow.setAttribute("d", `M${X(10)} ${Y(-2)} q${dir * 6} 4 ${dir * 12} 0`);
    f.mouth.setAttribute("d", mo);
    f.lash.setAttribute("d", L.lash && m !== "closed" ? `M${X(19)} ${Y(-7)} l${dir * 7} -4` : "");
    if (L.glasses) {
      f.lens.setAttribute("cx", X(16)); f.lens.setAttribute("cy", Y(-2));
      f.gframe.setAttribute("d", `M${X(6)} ${Y(-4)} L${X(-13)} ${Y(-2)} M${X(26)} ${Y(-4)} L${X(31)} ${Y(-3)}`);
    }
    // optional phone in the front hand (k.prop === "phone"), screen glow when k.glow
    if (k.prop === "phone") { f.prop.setAttribute("width", 26); f.prop.setAttribute("height", 46); f.prop.setAttribute("x", (hf[0] - 13).toFixed(1)); f.prop.setAttribute("y", (hf[1] - 30).toFixed(1)); }
    else { f.prop.setAttribute("width", 0); f.prop.setAttribute("height", 0); }
    f.glow.setAttribute("r", k.glow ? 90 : 0); f.glow.setAttribute("cx", hf[0].toFixed(1)); f.glow.setAttribute("cy", (hf[1] - 10).toFixed(1));
    const gy = k.anchor === "hip" ? 150 : 0;
    f.shadow.setAttribute("cx", "0"); f.shadow.setAttribute("cy", String(gy)); f.shadow.setAttribute("rx", "70"); f.shadow.setAttribute("ry", "12");
    f.shadow.setAttribute("opacity", k.anchor === "hip" ? 0 : 0.25);
    f.g.setAttribute("transform", `translate(${st.x.toFixed(1)} ${st.y.toFixed(1)}) rotate(${st.rot.toFixed(2)}) scale(${st.s.toFixed(3)})`);
  }
  return { P, fig, draw };
})();
// dust motes drift on a fixed path that is a function of time (same every render)
function DUST(sel, n, seed, box) {
  const g = document.querySelector(sel), ns = "http://www.w3.org/2000/svg", ds = [];
  const fr = (v) => v - Math.floor(v), rnd = (i) => fr(Math.sin((i + seed * 31) * 12.9898) * 43758.5453);
  for (let i = 0; i < n; i++) {
    const c = document.createElementNS(ns, "circle");
    c.setAttribute("r", (1.5 + rnd(i * 3) * 2.5).toFixed(1)); c.setAttribute("fill", box.col || "#ffe2a8");
    g.appendChild(c);
    ds.push({ c, x: box.x + rnd(i) * box.w, y: box.y + rnd(i * 7) * box.h, vx: (rnd(i * 5) - 0.5) * 14, vy: -6 - rnd(i * 11) * 12, ph: rnd(i * 13) * 6.28, a: 0.25 + rnd(i * 17) * 0.55 });
  }
  return { draw(t) { for (const d of ds) { const y = box.y + ((d.y - box.y + d.vy * t) % box.h + box.h) % box.h; d.c.setAttribute("cx", (d.x + d.vx * t + Math.sin(t * 0.8 + d.ph) * 10).toFixed(1)); d.c.setAttribute("cy", y.toFixed(1)); d.c.setAttribute("opacity", (d.a * (0.6 + 0.4 * Math.sin(t * 1.3 + d.ph))).toFixed(2)); } } };
}
"""

FONTS = """
    @font-face { font-family: "Kanit"; src: url("assets/fonts/Kanit-Bold.ttf"); font-weight: 700; }
    @font-face { font-family: "Kanit"; src: url("assets/fonts/Kanit-ExtraBold.ttf"); font-weight: 800; }
    @font-face { font-family: "Kanit"; src: url("assets/fonts/Kanit-Medium.ttf"); font-weight: 500; }
    @font-face { font-family: "Kanit"; src: url("assets/fonts/Kanit-Light.ttf"); font-weight: 300; }"""


def scene(sid, dur, css, svg, overlays, js, bg="#0b0d14"):
    return f"""<template>
  <style>{FONTS}
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {bg}; font-family: "Kanit", sans-serif; color: #fff; }}
    #{sid}-art {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <svg id="{sid}-art" viewBox="0 0 1080 1920">
{svg}
    </svg>
{overlays}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{RIG}
    let DUSTS = [];
{js}
    // one driver redraws characters and dust from timeline time
    const frame = (t) => {{ FIGS.forEach((f) => PERSON.draw(f, t)); DUSTS.forEach((d) => d.draw(t)); }};
    const drv = {{ t: 0 }};
    tl.to(drv, {{ t: {dur}, duration: {dur}, ease: "none", onUpdate: () => frame(drv.t) }}, 0);
    frame(0);
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
