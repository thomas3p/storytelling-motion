"""Sets of 60°C รุ่งอรุณเดือด (flood look, 1080 x 1920), as JS functions that run inside a flatkit scene and return SVG strings.
Each set splits into parallax layers <g id="${P}-far|mid|near"> so shot(dur, s, x, y, [["#P-far", 10], ["#P-near", -30]]) can
drift them at different speeds. Animated parts carry ids (P-sun, P-haze, P-ac, P-fan1 …); each set's comment lists them.
Character slots: pass `slot` (SVG drawn between the mid and near layers). Feet y ≈ 1190, subtitle band 1232–1400 (keep it dark).
"""

JS = r"""
    const R = (x, y, w, h, c, rx = 0, ex = "") => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${c}" ${ex} />`;
    const T = (x, y, s, c, txt, w = 700, anchor = "middle", ex = "") => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Prompt" font-weight="${w}" font-size="${Math.max(28, s)}" fill="${c}" data-layout-ignore ${ex}>${txt}</text>`;
    const grad = (id, stops, v = true) => { addDef(`<linearGradient id="${P}-${id}" x1="0" y1="0" x2="${v ? 0 : 1}" y2="${v ? 1 : 0}">${stops.map(([o, c, a = 1]) => `<stop offset="${o}" stop-color="${c}" stop-opacity="${a}" />`).join("")}</linearGradient>`); return `url(#${P}-${id})`; };
    const windows = (seed, n, x0, x1, y0, y1, c = "#ffcf7a", w = 14, h = 18) => { const r = rng(seed); let s = ""; for (let i = 0; i < n; i++) s += R(f1(x0 + r() * (x1 - x0)), f1(y0 + r() * (y1 - y0)), w, h, c, 0, `opacity="${f1(0.15 + r() * 0.5)}"`); return s; };
    // glare: a white-hot sun disc with a wide halo (id on the group so it can rise / pulse)
    const sunDisc = (x, y, r, id = `${P}-sun`) => `<g id="${id}">${glow(x, y, r * 5.2, "amber", 0.75)}${glow(x, y, r * 2.6, "warm", 0.95)}<circle cx="${x}" cy="${y}" r="${r}" fill="#fff6dc" /><circle cx="${x}" cy="${y}" r="${f1(r * 0.82)}" fill="#ffffff" /></g>`;
    // heat haze: soft wavy bands that drift up (animate the group P-haze: y and opacity)
    const haze = (y0, y1, n = 7, c = "#fff1c8", op = 0.12, id = `${P}-haze`) => { let s = ""; for (let i = 0; i < n; i++) { const y = y0 + (i * (y1 - y0)) / n; s += `<path d="M-40,${f1(y)} Q120,${f1(y - 26)} 270,${f1(y)} T580,${f1(y)} T890,${f1(y)} T1200,${f1(y)}" stroke="${c}" stroke-width="${10 + (i % 3) * 6}" fill="none" opacity="${op}" stroke-linecap="round" />`; } return `<g id="${id}">${s}</g>`; };
    // whole-frame heat grade: warm wash (soft-light) whose strength follows the temperature (0..1)
    const HEAT = (k, id = `${P}-heat`) => `<rect id="${id}" width="1080" height="1920" fill="#ff7a2a" style="mix-blend-mode: soft-light" opacity="${f1(0.15 + k * 0.55)}" /><rect width="1080" height="1920" fill="#ff5a2a" opacity="${f1(k * 0.08)}" />`;
    // a glass curtain wall panel grid (x, y, w, h, columns, rows), sky reflected as a vertical gradient
    const curtain = (x, y, w, h, cols, rows, fill, line = "#1d2a3a", lw = 4) => { let s = R(x, y, w, h, fill); for (let i = 1; i < cols; i++) s += `<path d="M${f1(x + (i * w) / cols)},${y} L${f1(x + (i * w) / cols)},${y + h}" stroke="${line}" stroke-width="${lw}" />`; for (let j = 1; j < rows; j++) s += `<path d="M${x},${f1(y + (j * h) / rows)} L${x + w},${f1(y + (j * h) / rows)}" stroke="${line}" stroke-width="${lw}" />`; return s; };
    // the ground-level city line seen from high up: far towers in a dawn haze
    const farCity = (seed, base, c1, c2, glassC = "#ffb070") => { const r = rng(seed); let s = "", x = -20; while (x < 1100) { const w = 70 + r() * 110, h = 160 + r() * 380; s += R(f1(x), f1(base - h), f1(w), f1(h + 400), r() > 0.5 ? c1 : c2); if (r() > 0.45) s += R(f1(x + 8), f1(base - h + 10), f1(w - 16), f1(h * 0.7), glassC, 0, `opacity="${f1(0.12 + r() * 0.2)}"`); x += w + 6; } return s; };

    // ── HOOK · dawn skyline: sky gradient, rising sun P-sun (behind the towers), far towers, a roadside digital billboard
    // (P-board, temperature text P-btemp), heat haze P-haze, rooftop edge in front.
    function skyline(slot = "") {
      const sky = grad("sky", [[0, "#24123a"], [0.38, "#7a2c4a"], [0.6, "#ff7a3a"], [0.74, "#ffc46a"], [1, "#ffe2a0"]]);
      return `<rect width="1080" height="1920" fill="${sky}" />
        <g id="${P}-far">${sunDisc(540, 1020, 120)}${farCity(7, 1060, "#4a2440", "#5a2a44", "#ff9a5a")}${haze(760, 1080, 6)}</g>
        <g id="${P}-mid">${farCity(19, 1200, "#2a1630", "#341a36", "#ffb070")}
          <g transform="translate(150 640)">${R(0, 0, 360, 230, "#0d0a14", 18)}${R(14, 14, 332, 202, "#1a0a0a", 10)}${glow(180, 115, 240, "red", 0.45)}
            ${T(180, 70, 32, "#ffcf8a", "อุณหภูมิตอนนี้")}<text id="${P}-btemp" x="180" y="186" text-anchor="middle" font-family="Mitr" font-weight="600" font-size="104" fill="#ff4636" data-layout-ignore>35°C</text>
            ${R(170, 230, 20, 260, "#0d0a14")}</g></g>
        ${slot}<g id="${P}-near"><path d="M0,1210 L1080,1180 L1080,1920 L0,1920 Z" fill="#120a14" />${R(0, 1180, 1080, 30, "#2a1a24")}
          ${[60, 300, 760, 1000].map((x) => R(x, 1110, 14, 80, "#2a1a24")).join("")}${R(0, 1100, 1080, 14, "#2a1a24")}</g>`;
    }

    // ── the glass condo from outside: a tall glass tower (floors as bands; floor 40 band P-f40), the sun P-sun at right,
    // neighbouring towers, haze P-haze. `hot` (0..1) makes the glass glow from inside like an oven (P-oven).
    function tower(hot = 0, slot = "") {
      const sky = grad("tsky", [[0, "#3a1a3e"], [0.5, "#ff8a4a"], [1, "#ffd28a"]]);
      const glass = grad("tglass", [[0, "#3a6a8a"], [0.45, "#7ab8d0"], [0.55, "#ffb070"], [1, "#2a4a62"]], false);
      let floors = ""; for (let i = 0; i < 26; i++) floors += `<path d="M330,${260 + i * 40} L750,${260 + i * 40}" stroke="#1d2a3a" stroke-width="3" opacity="0.7" />`;
      return `<rect width="1080" height="1920" fill="${sky}" />
        <g id="${P}-far">${sunDisc(900, 520, 80)}${farCity(31, 1240, "#4a2440", "#5a2a44")}${haze(400, 1200, 8, "#fff1c8", 0.1)}</g>
        <g id="${P}-mid">${R(80, 700, 200, 600, "#2a2236")}${windows(5, 30, 90, 270, 720, 1260, "#ffcf7a")}${R(820, 820, 220, 480, "#2a2236")}${windows(8, 26, 830, 1030, 840, 1280, "#ffcf7a")}
          <path d="M330,240 L540,140 L750,240 L750,1320 L330,1320 Z" fill="${glass}" />${curtain(330, 240, 420, 1080, 7, 27, "rgba(0,0,0,0)", "#1d2a3a", 3)}${floors}
          <path d="M330,240 L540,140 L750,240 Z" fill="#24364a" /><path d="M560,240 L750,240 L750,1320 L640,1320 Z" fill="#ffffff" opacity="0.12" />
          <g id="${P}-oven" opacity="${hot}">${R(330, 240, 420, 1080, "#ff5a2a", 0, 'style="mix-blend-mode: screen" opacity="0.55"')}${glow(540, 760, 520, "red", 0.5)}</g>
          <g id="${P}-f40">${R(326, 316, 428, 44, "#ffd27a", 4, 'opacity="0.0"')}<rect x="322" y="312" width="436" height="52" rx="6" fill="none" stroke="#ffcf6a" stroke-width="8" />${glow(540, 338, 260, "amber", 0.6)}</g></g>
        ${slot}<g id="${P}-near">${R(0, 1300, 1080, 620, "#1a1018")}${R(0, 1300, 1080, 620, SHV)}</g>`;
    }

    // ── the penthouse: a full glass wall at the back (sun P-sun rises behind it, sunbeams P-beam), wall AC unit at top left
    // (P-ac, louver P-acl, status LED P-acled), TV at right (screen group P-tv), sofa, a step ladder under the AC at x ~330.
    // Chain on the ladder: place at 330 / 1080 (s 0.92). Floor from y 1150 (dark wood, keeps the subtitle band dark).
    function penthouse(sunY = 1180, slot = "", tv = true) {
      const out = grad("psky", [[0, "#3a1a3e"], [0.55, "#ff8a4a"], [1, "#ffd28a"]]);
      const wall = grad("pwall", [[0, "#efe2d4"], [1, "#cdb8a6"]]), floor = grad("pfl", [[0, "#5a3a2a"], [0.3, "#2e1e18"], [1, "#120a08"]]);
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far">${R(40, 180, 1000, 970, out)}${sunDisc(700, sunY, 110)}${farCity(41, 1150, "#4a2440", "#5a2a44")}${haze(700, 1140, 6)}</g>
        <g id="${P}-mid">${curtain(40, 180, 1000, 970, 5, 1, "rgba(0,0,0,0)", "#d8cfc4", 16)}${R(28, 168, 1024, 20, "#d8cfc4")}${R(28, 1140, 1024, 20, "#b8a898")}
          <g id="${P}-beam">${cone(700, 900, 112, 1200, 60, "#fff1c8", 0.28)}${cone(700, 900, 140, 1100, 40, "#ffcf8a", 0.2)}</g>
          <g id="${P}-ac" transform="translate(330 300)">${R(-170, -60, 340, 120, "#f6f4f0", 26)}${R(-170, -60, 340, 120, SHV, 26)}<g id="${P}-acl">${R(-150, 30, 300, 16, "#c9c4bc", 8)}</g>
            <circle id="${P}-acled" cx="140" cy="-28" r="7" fill="#46e070" />${T(-120, -14, 28, "#9a948c", "AIR", 700, "start")}</g>
          ${tv ? `<g transform="translate(860 860)">${R(-140, -90, 280, 170, "#14161c", 12)}<g id="${P}-tv">${R(-128, -78, 256, 146, "#2a3a5a", 6)}</g>${R(-10, 80, 20, 60, "#2a2a30")}${R(-90, 136, 180, 14, "#2a2a30", 6)}</g>` : ""}
          ${R(0, 1150, 1080, 770, floor)}<ellipse cx="700" cy="1260" rx="420" ry="60" fill="#ffcf8a" opacity="0.14" />
          <g transform="translate(150 1150)">${R(-110, -110, 220, 110, "#8a5a4a", 20)}${R(-130, -150, 60, 150, "#7a4a3a", 20)}${R(70, -150, 60, 150, "#7a4a3a", 20)}</g></g>
        ${slot}<g id="${P}-near">${R(0, 1180, 1080, 740, "url(#" + P + "-shadeV)")}</g>`;
    }
    // an A-frame step ladder, origin = floor centre
    const ladder = (h = 520) => `<g><path d="M-90,0 L-30,${-h} M90,0 L30,${-h}" stroke="#b8bec8" stroke-width="16" stroke-linecap="round" />${[0.2, 0.42, 0.64, 0.86].map((k) => `<path d="M${f1(-90 + 60 * k)},${f1(-h * k)} L${f1(90 - 60 * k)},${f1(-h * k)}" stroke="#9aa2ae" stroke-width="12" stroke-linecap="round" />`).join("")}${R(-40, -h - 14, 80, 22, "#7a828e", 6)}</g>`;

    // ── the AC condensers on the service balcony: four outdoor units (P-u1..4, fans P-fan1..4, smoke P-sm1..4, blast P-bl1..4),
    // pipes, railing, the hot sky behind (P-sun high). Units at x 230/530/830 (row 1, y 760) and 380/680 (row 2, y 1100).
    function condensers(slot = "") {
      const sky = grad("csky", [[0, "#ff8a4a"], [0.6, "#ffcf8a"], [1, "#fff1c8"]]);
      const unit = (n, x, y, s) => { const fan = `<g id="${P}-fan${n}">${[0, 90, 180, 270].map((a) => `<path d="M0,0 Q30,-70 0,-86 Q-24,-60 0,0 Z" fill="#5a6676" transform="rotate(${a})" />`).join("")}<circle r="14" fill="#3a4250" /></g>`;
        return `<g transform="translate(${x} ${y}) scale(${s})"><g id="${P}-u${n}">${R(-130, -110, 260, 220, "#e8e4dc", 14)}${R(-130, -110, 260, 220, SH, 14)}<circle cx="-20" cy="0" r="92" fill="#4a5462" /><circle cx="-20" cy="0" r="80" fill="#2a3240" />
          <g transform="translate(-20 0)">${fan}</g>${[-60, -30, 0, 30, 60].map((dy) => `<path d="M-100,${dy} L60,${dy}" stroke="#8a929e" stroke-width="5" opacity="0.6" />`).join("")}${R(84, -90, 32, 180, "#c9c4bc", 6)}
          <g id="${P}-bl${n}" opacity="0">${glow(0, 0, 260, "amber", 1)}${glow(0, 0, 120, "white", 1)}<path d="M0,-150 L28,-40 L140,-60 L44,10 L120,110 L10,46 L-40,150 L-36,40 L-150,40 L-50,-20 L-120,-120 L-20,-56 Z" fill="#ffe08a" /></g>
          <g id="${P}-sm${n}" opacity="0">${[0, 1, 2].map((i) => `<circle cx="${-30 + i * 30}" cy="${-150 - i * 60}" r="${70 + i * 24}" fill="#2a2a30" opacity="0.7" />`).join("")}</g></g></g>`; };
      return `<rect width="1080" height="1920" fill="${sky}" />
        <g id="${P}-far">${sunDisc(820, 200, 90)}${farCity(57, 760, "#c8704a", "#d8805a", "#fff1c8")}${haze(300, 760, 6, "#ffffff", 0.14)}</g>
        <g id="${P}-mid">${R(0, 640, 1080, 1280, "#6a6260")}${R(0, 640, 1080, 1280, SHV)}${R(0, 630, 1080, 22, "#4a4442")}
          ${[160, 460, 760].map((x) => `<path d="M${x},860 Q${x},1000 ${x + 120},1000 L${x + 120},1240" stroke="#c88a5a" stroke-width="12" fill="none" />`).join("")}
          ${unit(1, 230, 760, 0.95)}${unit(2, 530, 760, 0.95)}${unit(3, 830, 760, 0.95)}${unit(4, 380, 1060, 1.1)}${unit(5, 700, 1060, 1.1)}</g>
        ${slot}<g id="${P}-near">${R(0, 1220, 1080, 700, "#1a1416")}${R(0, 1220, 1080, 700, SHV)}${[0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => R(i * 135, 1170, 12, 70, "#2a2224")).join("")}${R(0, 1162, 1080, 16, "#2a2224")}</g>`;
    }

    // ── the fact: a red sedan parked on asphalt under a white sun; a thermometer inside the cabin (mercury P-merc, label P-ct),
    // heat haze off the road P-haze, the sun P-sun top right. The car sits at y ~1110.
    function carlot(slot = "") {
      const sky = grad("lsky", [[0, "#ffb070"], [0.6, "#ffe0a8"], [1, "#fff4d8"]]);
      return `<rect width="1080" height="1920" fill="${sky}" />
        <g id="${P}-far">${sunDisc(860, 520, 90)}${R(0, 820, 1080, 120, "#d8a07a")}${farCity(63, 900, "#c8906a", "#d8a07a", "#fff1c8")}</g>
        <g id="${P}-mid">${R(0, 930, 1080, 990, "#3a3436")}${R(0, 930, 1080, 990, SHV)}${[120, 420, 720, 1020].map((x) => `<path d="M${x},930 L${x - 60},1240" stroke="#e8e0c8" stroke-width="8" opacity="0.5" />`).join("")}
          ${haze(900, 1120, 5, "#ffffff", 0.18)}
          <g transform="translate(540 1110)"><ellipse cx="0" cy="10" rx="420" ry="30" fill="#000" opacity="0.35" />
            <path d="M-400,-40 L-360,-150 Q-340,-190 -290,-196 L-170,-204 Q-110,-300 -20,-306 L170,-306 Q250,-300 300,-206 L370,-196 Q410,-170 410,-120 L410,-40 Z" fill="#c8243a" />
            <path d="M-400,-40 L-360,-150 Q-340,-190 -290,-196 L-170,-204 Q-110,-300 -20,-306 L170,-306 Q250,-300 300,-206 L370,-196 Q410,-170 410,-120 L410,-40 Z" fill="${SHV}" />
            <path d="M-150,-206 Q-100,-284 -20,-288 L60,-288 L60,-206 Z" fill="#9fd0ec" opacity="0.85" /><path d="M80,-288 L160,-288 Q230,-282 274,-206 L80,-206 Z" fill="#9fd0ec" opacity="0.85" />
            <g transform="translate(20 -248)">${R(-12, -32, 24, 64, "#f2ead6", 12)}<circle cx="0" cy="34" r="16" fill="#e5483a" /><rect id="${P}-merc" x="-5" y="-20" width="10" height="54" rx="5" fill="#e5483a" style="transform-origin: 0px 34px" /></g>
            ${R(-410, -60, 820, 30, "#a81c30", 12)}${[-250, 250].map((x) => `<circle cx="${x}" cy="-30" r="70" fill="#1e1e22" /><circle cx="${x}" cy="-30" r="30" fill="#9a9aa0" />`).join("")}
            <path d="M-300,-200 L280,-200" stroke="#ffffff" stroke-width="5" opacity="0.4" /></g></g>
        ${slot}<g id="${P}-near">${R(0, 1180, 1080, 740, "#221e20")}${R(0, 1180, 1080, 740, SHV)}</g>`;
    }

    // ── the bathroom: tiles, mirror, a chrome tap P-tap over a white basin, water stream P-water, boiling bubbles P-bub,
    // steam P-steam, a narrow window strip with harsh light P-win. Chain stands at x ~300 (feet 1190).
    function bathroom(slot = "") {
      const wall = grad("bwall", [[0, "#e8f0f0"], [1, "#b8c8cc"]]);
      let tiles = ""; for (let y = 120; y < 1180; y += 80) tiles += `<path d="M0,${y} L1080,${y}" stroke="#c4d2d6" stroke-width="4" />`; for (let x = 0; x < 1080; x += 80) tiles += `<path d="M${x},0 L${x},1180" stroke="#c4d2d6" stroke-width="4" />`;
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far">${tiles}<g id="${P}-win">${R(760, 160, 260, 120, "#fff6dc")}${glow(890, 220, 260, "warm", 0.8)}${cone(890, 280, 115, 900, 40, "#fff1c8", 0.25)}</g>
          ${R(520, 340, 400, 420, "#9fb8c4", 20)}${R(536, 356, 368, 388, "#cfe2ea", 14)}<path d="M560,380 L640,380 L560,520 Z" fill="#ffffff" opacity="0.5" /></g>
        <g id="${P}-mid">${R(0, 1180, 1080, 740, "#2a3236")}
          ${R(460, 860, 520, 60, "#f4f4f2", 14)}${R(460, 920, 520, 260, "#d8dcdc")}${R(460, 920, 520, 260, SH)}
          <ellipse cx="720" cy="880" rx="200" ry="34" fill="#c8d0d2" /><ellipse cx="720" cy="884" rx="180" ry="26" fill="#a8b8bc" />
          <g id="${P}-bub">${[[-120, 0, 14], [-60, 6, 18], [0, -2, 12], [60, 4, 16], [120, 0, 12], [-90, 8, 10], [90, 8, 10], [30, 6, 20]].map(([x, y, r]) => `<circle cx="${720 + x}" cy="${884 + y}" r="${r}" fill="#ffffff" opacity="0.85" />`).join("")}</g>
          <g id="${P}-tap" transform="translate(720 760)">${R(-16, 0, 32, 80, "#c8d0d8", 10)}<path d="M-16,10 Q-16,-30 30,-30 L90,-30 L90,-6 L36,-6 Q14,-6 14,10 Z" fill="#d8e0e8" />${R(-40, 64, 80, 24, "#b8c0c8", 8)}</g>
          <path id="${P}-water" d="M792,744 L798,884" stroke="#bfe6ff" stroke-width="14" stroke-linecap="round" opacity="0.9" />
          <g id="${P}-steam">${[0, 1, 2, 3].map((i) => `<path d="M${640 + i * 50},860 Q${610 + i * 50},780 ${650 + i * 50},720 Q${690 + i * 50},660 ${650 + i * 50},590" stroke="#ffffff" stroke-width="${22 - i * 3}" fill="none" stroke-linecap="round" opacity="0.5" />`).join("")}</g></g>
        ${slot}<g id="${P}-near">${R(0, 1180, 1080, 740, SHV)}</g>`;
    }

    // ── looking out through the glass wall: big panes (mullions), white-hot sky, the city far below, birds fall in P-birds
    // (drawn by the scene), heat haze P-haze. Chain's back/silhouette goes in `slot` at the bottom.
    function glassView(slot = "") {
      const sky = grad("gsky", [[0, "#ffb070"], [0.5, "#ffe2a8"], [1, "#fff6e0"]]);
      return `<rect width="1080" height="1920" fill="${sky}" />
        <g id="${P}-far">${sunDisc(300, 300, 100)}${farCity(71, 1300, "#d89a7a", "#c88a6a", "#fff1c8")}${haze(500, 1280, 8, "#ffffff", 0.14)}<g id="${P}-birds"></g></g>
        <g id="${P}-mid">${curtain(-10, -10, 1100, 1240, 3, 2, "rgba(0,0,0,0)", "#2a2224", 26)}${R(-10, 1210, 1100, 30, "#2a2224")}<path d="M120,120 L320,120 L140,520 Z" fill="#ffffff" opacity="0.18" /><path d="M760,700 L900,700 L780,980 Z" fill="#ffffff" opacity="0.12" /></g>
        ${slot}<g id="${P}-near">${R(0, 1230, 1080, 690, "#1a1214")}${R(0, 1230, 1080, 690, SHV)}</g>`;
    }

    // ── the lift hall in a blackout: two lift doors (indicator P-ind with text P-indt), the fire-exit door at right with a green
    // EXIT sign P-exit, a red emergency light P-emer, ceiling lights P-lights (fade them out for the blackout), a dark overlay P-dark.
    // Chain stands at x ~540 (feet 1190).
    function liftHall(slot = "") {
      const wall = grad("hwall", [[0, "#d8d0c8"], [1, "#a89a90"]]);
      const door = (x) => `<g transform="translate(${x} 0)">${R(-150, 560, 300, 620, "#b8bcc4", 6)}${R(-146, 564, 144, 612, "#c9cdd4")}${R(2, 564, 144, 612, "#c9cdd4")}${R(-146, 564, 292, 612, SH)}${R(-160, 548, 320, 16, "#8a8e96")}</g>`;
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far"><g id="${P}-lights">${[300, 780].map((x) => `${R(x - 120, 120, 240, 20, "#fff8e8", 10)}${cone(x, 140, 90, 900, 70, "#fff1c8", 0.18)}`).join("")}</g>
          ${door(250)}${door(620)}<g id="${P}-ind" transform="translate(435 470)">${R(-80, -36, 160, 64, "#14161c", 10)}<text id="${P}-indt" x="0" y="14" text-anchor="middle" font-family="Mitr" font-weight="600" font-size="44" fill="#ff4636" data-layout-ignore>40</text></g>
          ${R(870, 560, 190, 620, "#05060a", 6)}<g id="${P}-fdoor">${R(870, 560, 190, 620, "#7a3a2a", 6)}${R(870, 560, 190, 620, SH, 6)}${R(1030, 860, 16, 60, "#c9a24a", 6)}</g>
          <g id="${P}-exit" transform="translate(965 480)">${R(-80, -32, 160, 60, "#0e3a24", 8)}${T(0, 10, 30, "#46e070", "EXIT")}${glow(0, 0, 140, "green", 0.55)}</g>
          ${T(965, 620, 28, "#ffe9d0", "ทางหนีไฟ")}</g>
        <g id="${P}-mid">${R(0, 1180, 1080, 740, "#3a3236")}${R(0, 1180, 1080, 740, SHV)}</g>
        ${slot}<g id="${P}-near"><rect id="${P}-dark" width="1080" height="1920" fill="#05060a" opacity="0" />
          <g id="${P}-emer" opacity="0">${glow(100, 200, 380, "red", 0.7)}${R(80, 180, 40, 30, "#ff4636", 8)}</g></g>`;
    }

    // ── the intercom panel, close: speaker grille, a small screen P-scr (caller text P-scrt), red call LED P-led, a dark hallway
    // with red emergency light P-emer. The panel sits at 540, 780.
    function intercomWall(slot = "") {
      const wall = grad("iwall", [[0, "#1a1418"], [1, "#0a080a"]]);
      let holes = ""; for (let y = 0; y < 6; y++) for (let x = 0; x < 7; x++) holes += `<circle cx="${-120 + x * 40}" cy="${-150 + y * 34}" r="9" fill="#0a0a0e" />`;
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far"><g id="${P}-emer">${glow(900, 260, 520, "red", 0.45)}</g>${R(0, 1180, 1080, 740, "#0c0a0c")}</g>
        <g id="${P}-mid"><g transform="translate(540 760)">${R(-230, -330, 460, 680, "#c9cdd4", 40)}${R(-230, -330, 460, 680, SH, 40)}${R(-200, -300, 400, 620, "#b0b4bc", 30)}
          ${holes}<g id="${P}-scr">${R(-150, 60, 300, 120, "#0a0e14", 10)}<text id="${P}-scrt" x="0" y="138" text-anchor="middle" font-family="Mitr" font-weight="600" font-size="58" fill="#ff4636" data-layout-ignore>B2</text></g>
          <g id="${P}-led"><circle cx="0" cy="240" r="22" fill="#ff3030" />${glow(0, 240, 120, "eye", 0.9)}</g>${R(-150, 210, 90, 60, "#9aa0aa", 12)}${R(60, 210, 90, 60, "#9aa0aa", 12)}</g></g>
        ${slot}<g id="${P}-near">${R(0, 1180, 1080, 740, SHV)}</g>`;
    }

    // ── the fire stairs from above: square landings shrinking toward a dark centre (a drop of 40 floors), handrail, floor numbers,
    // a red glow far below P-deep, flicker light P-lamp.
    function stairWell(slot = "") {
      let s = ""; const n = 11;
      for (let i = 0; i < n; i++) { const k = Math.pow(0.78, i), w = 1000 * k, h = 1500 * k, x = 540 - w / 2, y = 900 - h / 2, c = Math.round(200 * Math.pow(0.72, i));
        s += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(w)}" height="${f1(h)}" fill="rgb(${c},${Math.round(c * 0.9)},${Math.round(c * 0.86)})" />`;
        s += `<rect x="${f1(x + w * 0.08)}" y="${f1(y + h * 0.08)}" width="${f1(w * 0.84)}" height="${f1(h * 0.84)}" fill="none" stroke="#c8a24a" stroke-width="${f1(10 * k + 1)}" opacity="${f1(0.9 * Math.pow(0.8, i))}" />`;
        if (i < 4) s += `<text x="${f1(x + w * 0.16)}" y="${f1(y + h * 0.2)}" font-family="Mitr" font-weight="600" font-size="${f1(Math.max(28, 90 * k))}" fill="#3a2a24" opacity="0.7" data-layout-ignore>${40 - i}</text>`; }
      return `<rect width="1080" height="1920" fill="#0a0808" />
        <g id="${P}-far">${s}<g id="${P}-deep">${glow(540, 900, 260, "red", 0.9)}</g></g>
        <g id="${P}-mid"><g id="${P}-lamp">${glow(200, 260, 420, "warm", 0.35)}</g></g>
        ${slot}<g id="${P}-near">${R(0, 1180, 1080, 740, "#0a0808", 0, 'opacity="0.5"')}</g>`;
    }
"""
