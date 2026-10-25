"""Sets of ปอบยุค 5G (flood look, 1080 x 1920), as JS functions that run inside a flatkit scene and return SVG strings.
Each set splits into parallax layers <g id="${P}-far|mid|near"> so shot(dur, s, x, y, [["#P-far", 10], ["#P-near", -30]]) can
drift them at different speeds. Light elements carry ids (P-lamp, P-neon, P-tube …) for flicker().
Character slots: pass `slot` (SVG drawn between the mid and near layers, e.g. a person behind a table) or append after the set;
place(person(...).svg, x, y, s, id) where the comment of each set says (feet y ≈ 1190, subtitle band 1232–1400).
"""

JS = r"""
    const R = (x, y, w, h, c, rx = 0, ex = "") => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${c}" ${ex} />`;
    const T = (x, y, s, c, txt, w = 700, anchor = "middle", ex = "") => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Prompt" font-weight="${w}" font-size="${Math.max(28, s)}" fill="${c}" data-layout-ignore ${ex}>${txt}</text>`;
    const grad = (id, stops, v = true) => { addDef(`<linearGradient id="${P}-${id}" x1="0" y1="0" x2="${v ? 0 : 1}" y2="${v ? 1 : 0}">${stops.map(([o, c, a = 1]) => `<stop offset="${o}" stop-color="${c}" stop-opacity="${a}" />`).join("")}</linearGradient>`); return `url(#${P}-${id})`; };
    const windows = (seed, n, x0, x1, y0, y1, c = "#ffcf7a") => { const r = rng(seed); let s = ""; for (let i = 0; i < n; i++) s += R(f1(x0 + r() * (x1 - x0)), f1(y0 + r() * (y1 - y0)), 14, 18, c, 0, `opacity="${f1(0.15 + r() * 0.5)}"`); return s; };
    // a biohazard mark (three rings around a dot)
    const bio = (x, y, s, c) => `<g transform="translate(${x} ${y}) scale(${s})" fill="none" stroke="${c}" stroke-width="7">${[0, 120, 240].map((a) => `<circle cx="${f1(Math.sin(a * D) * 16)}" cy="${f1(-Math.cos(a * D) * 16)}" r="15" />`).join("")}<circle r="6" fill="${c}" stroke="none" /></g>`;
    // red infectious-waste bin with lid (id for the lid so it can open)
    const bin = (id, x, y, s = 1, open = 0) => `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-80,0 L-70,-210 L70,-210 L80,0 Z" fill="#c8243a" /><path d="M-80,0 L-70,-210 L70,-210 L80,0 Z" fill="${SH}" />
      ${R(-60, -190, 120, 22, "#a81c30", 6)}${bio(0, -112, 1, "#ffe9e9")}${T(0, -40, 22, "#ffe9e9", "ขยะติดเชื้อ")}
      <g id="${id}" transform="rotate(${open} -84 -214)"><path d="M-86,-206 L-84,-232 Q0,-246 84,-232 L86,-206 Z" fill="#a81c30" />${R(-26, -250, 52, 16, "#8a1626", 6)}</g></g>`;

    // ── สมัยก่อน: a night village, moon, stilt houses, torches (hook). Granny at x ~600 feet 1190, chicken slot P-hen.
    function village(slot = "") {
      const sky = grad("vsky", [[0, "#140f28"], [1, "#3a2a3e"]]), ground = grad("vgr", [[0, "#2a2030"], [1, "#0e0a12"]]);
      const house = (x, y, w, c) => `<g><path d="M${x - 20},${y} L${x + w / 2},${y - 120} L${x + w + 20},${y} Z" fill="${c}" />${R(x, y, w, 150, c)}${R(x + w * 0.3, y + 40, 40, 50, "#ffb05a", 4, 'opacity="0.55"')}${[0, 1, 2, 3].map((i) => R(x + 10 + i * (w - 30) / 3, y + 150, 10, 140, c)).join("")}</g>`;
      const torch = (x, y) => `<g>${R(x - 4, y, 8, 120, "#3a2a20")}${glow(x, y - 10, 120, "amber", 0.8)}<path class="${P}-fl" d="M${x - 14},${y} Q${x},${y - 56} ${x + 14},${y} Z" fill="#ffcf6a" /></g>`;
      const villager = (x, y, s) => `<g transform="translate(${x} ${y}) scale(${s})" fill="#120c18"><circle cx="0" cy="-330" r="44" /><path d="M-60,-280 Q0,-300 60,-280 L66,-110 L-66,-110 Z" /><rect x="-46" y="-120" width="34" height="120" rx="14" /><rect x="12" y="-120" width="34" height="120" rx="14" /><path d="M-70,-372 Q0,-430 70,-372 Q0,-388 -70,-372 Z" /></g>`;
      return `<rect width="1080" height="1920" fill="${sky}" />
        <g id="${P}-far">${glow(820, 380, 260, "warm", 0.35)}<circle cx="820" cy="380" r="90" fill="#f6e6c0" /><circle cx="790" cy="360" r="16" fill="#e2cfa0" /><circle cx="846" cy="410" r="10" fill="#e2cfa0" />
          <path d="M0,900 Q200,780 420,860 Q640,760 860,850 Q980,800 1080,830 L1080,1100 L0,1100 Z" fill="#1c1428" />
          ${house(60, 820, 220, "#1a1222")}${house(720, 840, 240, "#1a1222")}</g>
        <g id="${P}-mid">${villager(260, 1080, 0.8)}${torch(320, 760)}${villager(860, 1090, 0.85)}${torch(800, 760)}${villager(430, 1060, 0.7)}</g>
        ${slot}<g id="${P}-near"><path d="M0,1080 Q540,1050 1080,1080 L1080,1920 L0,1920 Z" fill="${ground}" /><path d="M300,1920 Q480,1300 540,1090 Q600,1300 780,1920 Z" fill="#3a2c34" opacity="0.6" />
          ${[[120, 1180], [960, 1200], [200, 1500], [900, 1560]].map(([x, y]) => `<path d="M${x},${y} l-14,-40 l10,8 l6,-46 l8,40 l12,-30 l-2,68 Z" fill="#1e2a1c" />`).join("")}</g>
        <rect width="1080" height="1920" fill="#c8964a" opacity="0.12" />`;
    }
    // a white chicken running (front-ish, flapping), origin = feet
    const hen = () => `<g><ellipse cx="0" cy="-60" rx="56" ry="46" fill="#f4efe6" /><ellipse cx="0" cy="-60" rx="56" ry="46" fill="${SH}" /><circle cx="22" cy="-118" r="28" fill="#f4efe6" />
      <path d="M16,-146 q6,-16 14,-2 q6,-14 12,2 Z" fill="#e5483a" /><path d="M46,-116 l18,6 l-18,6 Z" fill="#f2b83a" /><circle cx="30" cy="-122" r="4" fill="#24160f" /><path d="M40,-100 q6,8 0,16" stroke="#e5483a" stroke-width="6" fill="none" />
      <g id="${P}-wing"><path d="M-30,-70 Q-90,-110 -96,-50 Q-60,-60 -30,-40 Z" fill="#e8e0d2" /></g><path d="M-10,-16 L-14,0 M12,-16 L16,0" stroke="#f2b83a" stroke-width="6" stroke-linecap="round" /></g>`;

    // ── the city at night: skyline, 5G mast (P-w1..3 waves, P-mast light), the clinic with a pink neon sign (P-neon) and an LED clock
    function clinicExt(clock = "23:47", day = false, slot = "") {
      const sky = day ? grad("csky", [[0, "#9fd0ec"], [1, "#fbe6cf"]]) : grad("csky", [[0, "#070a1c"], [1, "#24163e"]]);
      const bldg = day ? "#8a9ab0" : "#121a30", walk = day ? "#5e5856" : "#1a1724";
      const c = led(clock, 70, "#ff4636"), cw = c.w;
      return `<rect width="1080" height="1920" fill="${sky}" />
        <g id="${P}-far">${day ? glow(880, 300, 300, "warm", 0.5) : ""}
          <path d="M-20,1000 L-20,640 L90,640 L90,560 L220,560 L220,700 L330,700 L330,520 L470,520 L470,660 L620,660 L620,600 L780,600 L780,520 L900,520 L900,640 L1100,640 L1100,1000 Z" fill="${bldg}" />
          ${day ? "" : windows(21, 40, 0, 1080, 540, 960)}
          <g transform="translate(150 260)"><path d="M-40,420 L0,0 L40,420 Z M-28,300 L28,300 M-18,180 L18,180 M-10,80 L10,80" stroke="${day ? "#5a6a7e" : "#3a4466"}" stroke-width="8" fill="none" />
            ${R(-26, 40, 18, 40, day ? "#d8dce2" : "#8a94b0", 4)}${R(8, 40, 18, 40, day ? "#d8dce2" : "#8a94b0", 4)}
            <circle id="${P}-mast" cx="0" cy="-6" r="9" fill="#ff4636" />${day ? "" : glow(0, -6, 50, "red", 0.8, `id="${P}-mastg"`)}
            ${[1, 2, 3].map((i) => `<path id="${P}-w${i}" d="M${-30 - i * 26},${-30 - i * 10} Q0,${-70 - i * 26} ${30 + i * 26},${-30 - i * 10}" stroke="${day ? "#3a8ad0" : "#7fd6ff"}" stroke-width="6" fill="none" stroke-linecap="round" opacity="0" />`).join("")}
            ${T(0, 470, 30, day ? "#3a4a5e" : "#7fd6ff", "5G")}</g></g>
        <g id="${P}-mid">
          ${R(330, 430, 620, 780, day ? "#f4efec" : "#2a2238")}${R(330, 430, 620, 780, SH)}
          ${R(360, 470, 560, 150, day ? "#e9d6dc" : "#1a1424", 18)}
          <g id="${P}-neon">${day ? "" : glow(640, 545, 330, "neon", 0.55)}${T(640, 572, 74, day ? "#c8243a" : "#ff9cc2", "คลินิกหมอพิม", 700, "middle", day ? "" : `stroke="#ff3d7f" stroke-width="3"`)}</g>
          ${R(400, 660, 480, 330, day ? "#cfe4ee" : "#ffd0e0", 10, day ? "" : 'opacity="0.85"')}${day ? "" : glow(640, 820, 320, "pink", 0.45, `id="${P}-winglow"`)}
          ${R(400, 660, 480, 330, "url(#" + P + "-shadeV)", 10)}${R(632, 660, 16, 330, day ? "#9aa8b4" : "#3a2a3a")}
          <g transform="translate(${640 - cw / 2} 1030)">${R(-30, -24, cw + 60, 118, "#0a0a10", 16)}<g filter="url(#${P}-blur10)" opacity="0.8">${c.svg}</g>${c.svg}</g>
          ${R(300, 1190, 680, 22, day ? "#a8a29e" : "#3a3446")}</g>
        ${slot}<g id="${P}-near"><rect x="0" y="1200" width="1080" height="720" fill="${walk}" />${R(0, 1200, 1080, 720, "url(#" + P + "-shadeV)")}
          ${R(1000, 520, 14, 690, day ? "#5a6068" : "#0d1020")}${R(940, 510, 80, 16, day ? "#5a6068" : "#0d1020", 6)}
          ${day ? "" : `<g id="${P}-lamp">${cone(960, 530, 100, 700, 44, "#ffcf8a", 0.3)}${glow(960, 526, 90, "amber", 0.9)}</g>`}
          <path d="M0,1600 L1080,1600" stroke="${day ? "#d8d2cc" : "#2a2636"}" stroke-width="10" stroke-dasharray="80 60" /></g>`;
    }

    // ── clinic lobby (evening light): reception at left (cat slot P-cat at 230,880), pendant lamps P-l1..3, posters, queue board P-board.
    // Pim at 540/1190, clients queue at right (x 760–960, feet ~1150, s 0.72)
    function lobby(slot = "") {
      const wall = grad("lwall", [[0, "#f2e2e0"], [1, "#d7bfbd"]]), floor = grad("lfl", [[0, "#cdbab6"], [0.25, "#6a5450"], [1, "#2a2020"]]);
      const poster = (x, y) => `<g>${R(x, y, 150, 200, "#ffffff", 10)}${R(x + 12, y + 12, 60, 150, "#e8c8c8", 6)}${R(x + 78, y + 12, 60, 150, "#f6dede", 6)}<circle cx="${x + 42}" cy="${y + 50}" r="18" fill="#c89a8a" /><circle cx="${x + 108}" cy="${y + 50}" r="18" fill="#e8b4a4" />${T(x + 42, y + 186, 22, "#8a5a5a", "ก่อน")}${T(x + 108, y + 186, 22, "#c8243a", "หลัง")}</g>`;
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far">${poster(380, 300)}${poster(560, 300)}
          ${R(760, 290, 250, 220, "#fbf3dc", 18)}${R(760, 290, 250, 56, "#c8243a", 18)}${R(760, 326, 250, 20, "#c8243a")}${T(885, 330, 30, "#ffffff", "คิวผ่าตัด")}
          <g id="${P}-board">${T(885, 410, 34, "#1b2440", "ว่างถัดไป")}${T(885, 476, 54, "#c8243a", "ปีหน้า")}</g>
          ${[300, 540, 780].map((x, i) => `<g id="${P}-l${i + 1}"><path d="M${x},0 L${x},150" stroke="#8a6a5a" stroke-width="4" /><path d="M${x - 50},190 Q${x},120 ${x + 50},190 Z" fill="#c8a07a" />${glow(x, 200, 160, "warm", 0.7)}</g>`).join("")}</g>
        <g id="${P}-mid">${R(0, 1100, 1080, 820, floor)}
          ${R(40, 900, 360, 290, "#fbf7f4", 20)}${R(40, 900, 360, 290, SH, 20)}${R(40, 980, 360, 26, "#e88aa8")}${R(30, 884, 380, 30, "#e8dcd8", 12)}
          <circle cx="220" cy="1080" r="44" fill="#e88aa8" />${T(220, 1098, 50, "#ffffff", "P")}
          <g transform="translate(990 1190)"><path d="M-40,0 L-30,-120 L30,-120 L40,0 Z" fill="#d8c8b8" /><path d="M0,-120 Q-90,-250 -40,-360 Q-10,-240 0,-120 Q30,-300 80,-330 Q40,-200 0,-120 Q60,-220 110,-200 Q50,-150 0,-120 Z" fill="#5a9a6a" /></g></g>
        ${slot}<g id="${P}-near"><path d="M0,1190 L1080,1190" stroke="#c8b0ac" stroke-width="4" /><ellipse cx="540" cy="1500" rx="600" ry="120" fill="#ffffff" opacity="0.08" /></g>`;
    }

    // ── operating theatre: surgical lamp P-lamp, monitor with ECG P-ecg, lipo canister with fat level P-fat, patient under a sheet.
    // Pim (PIM_OR) at 560 feet 1300 s 1.05 — the table covers her legs
    function oroom(slot = "") {
      const wall = grad("owall", [[0, "#1c3a44"], [1, "#0c1a20"]]);
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far">${R(60, 640, 220, 170, "#0a1418", 12)}${R(72, 652, 196, 146, "#06100c", 8)}<path id="${P}-ecg" d="M80,760 L130,760 L145,710 L160,800 L175,740 L190,760 L260,760" stroke="#46e070" stroke-width="5" fill="none" />${glow(170, 745, 130, "green", 0.35)}
          ${T(170, 700, 30, "#46e070", "98 bpm", 700)}
          ${R(860, 380, 10, 520, "#8aa0a8")}${R(812, 400, 100, 140, "#e8f4f8", 18, 'opacity="0.8"')}${R(830, 470, 64, 60, "#c8243a", 10, 'opacity="0.7"')}</g>
        <g id="${P}-mid"><g id="${P}-lamp"><path d="M540,0 L540,150" stroke="#5a6a70" stroke-width="16" /><ellipse cx="540" cy="200" rx="190" ry="60" fill="#c8d8dc" /><ellipse cx="540" cy="214" rx="150" ry="36" fill="#fffbe8" />
            ${cone(540, 220, 90, 900, 52, "#fff6dc", 0.4)}${glow(540, 214, 220, "white", 0.55)}</g></g>
        ${slot}<g id="${P}-near">
          ${R(150, 1160, 780, 70, "#e8eef0", 14)}<path d="M150,1180 Q540,1080 930,1180 L930,1240 L150,1240 Z" fill="#3f9aa8" /><path d="M150,1180 Q540,1080 930,1180 L930,1240 L150,1240 Z" fill="${SH}" />
          ${R(300, 1230, 40, 300, "#5a6a70")}${R(740, 1230, 40, 300, "#5a6a70")}
          <g transform="translate(920 1150)">${R(-60, -260, 120, 260, "#dfeef2", 20, 'opacity="0.85"')}<clipPath id="${P}-cc"><rect x="-56" y="-256" width="112" height="252" rx="18" /></clipPath>
            <g clip-path="url(#${P}-cc)"><rect id="${P}-fat" x="-60" y="-60" width="120" height="260" fill="#f2d27a" /></g>${R(-60, -260, 120, 260, SH, 20)}${R(-30, -290, 60, 34, "#5a6a70", 8)}
            ${[-200, -140, -80].map((y) => `<path d="M30,${y} L56,${y}" stroke="#5a6a70" stroke-width="4" />`).join("")}${T(0, 40, 26, "#f2d27a", "ไขมัน")}</g></g>`;
    }

    // ── clinic corridor at night: tube light P-tube, EXIT sign, the waste-room door (red sign) at right, LED clock on the wall.
    // Pim walks toward the camera along x ~540 (feet 1190)
    function corridor(clock = "02:13", slot = "") {
      const wall = grad("cwall", [[0, "#141a2e"], [1, "#080b16"]]), fl = grad("cfl", [[0, "#1a2236"], [1, "#05070d"]]);
      const c = led(clock, 56, "#ff4636");
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far"><path d="M300,1000 L780,1000 L780,520 L300,520 Z" fill="#0b1020" />${R(470, 600, 140, 330, "#101830")}
          <g transform="translate(${540 - c.w / 2} 420)">${R(-20, -16, c.w + 40, 88, "#05060a", 12)}<g filter="url(#${P}-blur10)" opacity="0.8">${c.svg}</g>${c.svg}</g>
          ${R(490, 540, 100, 40, "#0e3a24", 6)}${T(540, 570, 26, "#46e070", "EXIT")}${glow(540, 560, 90, "green", 0.4)}</g>
        <g id="${P}-mid"><path d="M0,0 L300,520 L300,1000 L0,1500 Z" fill="#10162a" /><path d="M1080,0 L780,520 L780,1000 L1080,1500 Z" fill="#121a30" />
          <path d="M840,560 L1000,330 L1000,1250 L840,1060 Z" fill="#2a1420" />
          <g transform="translate(905 625) skewY(-22)">${R(-50, -30, 110, 54, "#c8243a", 6)}${T(5, 6, 22, "#ffe9e9", "ห้องขยะ")}</g>
          <g id="${P}-tube">${R(380, 120, 320, 18, "#dfe9ff", 9)}${cone(540, 140, 90, 900, 70, "#bcd6ff", 0.16)}${glow(540, 130, 200, "cold", 0.5)}</g></g>
        ${slot}<g id="${P}-near"><path d="M0,1500 L300,1000 L780,1000 L1080,1500 L1080,1920 L0,1920 Z" fill="${fl}" /><path d="M540,1000 L540,1920" stroke="#1e2a44" stroke-width="3" opacity="0.6" /></g>`;
    }

    // ── the waste room: tiles, two red bins (lids P-lid1/P-lid2), sharps box, tube light P-tube. night=true for blue-red gloom.
    // A person stands at x ~360 feet 1190; bins at 640 and 860
    function wasteRoom(night = true, slot = "", bins = true) {
      const wall = night ? grad("wwall", [[0, "#1a2232"], [1, "#0a0e18"]]) : grad("wwall", [[0, "#dfe8ec"], [1, "#a8b8c0"]]);
      let tiles = ""; for (let y = 140; y < 1180; y += 90) tiles += `<path d="M0,${y} L1080,${y}" stroke="${night ? "#222c40" : "#c4d2d8"}" stroke-width="4" />`;
      for (let x = 0; x < 1080; x += 90) tiles += `<path d="M${x},0 L${x},1180" stroke="${night ? "#222c40" : "#c4d2d8"}" stroke-width="4" />`;
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far">${tiles}${R(80, 420, 260, 24, night ? "#3a4256" : "#9aa8b0")}${R(100, 360, 80, 60, "#f2c14e", 8)}${R(200, 380, 110, 40, night ? "#e8e8e8" : "#ffffff", 6)}
          ${R(720, 300, 280, 90, night ? "#2a1a24" : "#c8243a", 10)}${T(860, 360, 38, "#ffe9e9", "ขยะติดเชื้อ")}</g>
        <g id="${P}-mid"><g id="${P}-tube">${R(380, 110, 320, 18, night ? "#cfe0ff" : "#ffffff", 9)}${cone(540, 130, 90, 1000, 80, night ? "#bcd6ff" : "#ffffff", night ? 0.18 : 0.25)}${glow(540, 120, 220, "cold", night ? 0.55 : 0.3)}</g>
          ${R(0, 1180, 1080, 740, night ? "#0c1220" : "#4a5860")}${R(0, 1180, 1080, 740, "url(#" + P + "-shadeV)")}</g>
        ${slot}<g id="${P}-near">${night ? glow(750, 1060, 360, "red", 0.25) : ""}${bins ? bin(`${P}-lid1`, 640, 1190, 1.15) + bin(`${P}-lid2`, 880, 1190, 1.0) + '<ellipse cx="760" cy="1196" rx="300" ry="20" fill="#000" opacity="0.25" />' : ""}</g>`;
    }

    // ── Pim's office at night: window with city lights, desk lamp P-lamp, diplomas; the 5 L canister + straw at 760,1110 (P-can level P-canfat)
    function office(slot = "") {
      const wall = grad("ofw", [[0, "#24142a"], [1, "#100810"]]);
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far">${R(90, 260, 900, 560, "#0a0c1c", 14)}${windows(33, 46, 100, 980, 520, 800, "#ffcf7a")}<path d="M90,820 L90,600 L220,600 L220,520 L360,520 L360,640 L520,640 L520,560 L700,560 L700,620 L860,620 L860,540 L990,540 L990,820 Z" fill="#14162a" opacity="0.8" />
          ${R(90, 260, 900, 560, "url(#" + P + "-shadeV)", 14)}${R(530, 260, 20, 560, "#1a0e1a")}</g>
        <g id="${P}-mid">${R(120, 880, 160, 120, "#e8d8b8", 6)}${R(134, 894, 132, 92, "#fbf3dc", 4)}${R(780, 880, 160, 120, "#e8d8b8", 6)}${R(794, 894, 132, 92, "#fbf3dc", 4)}</g>
        ${slot}<g id="${P}-near">${R(60, 1120, 960, 60, "#3a1e28", 10)}${R(60, 1180, 960, 740, "#22121a")}${R(60, 1180, 960, 740, "url(#" + P + "-shadeV)")}
          <g id="${P}-lamp"><path d="M230,1120 L250,1000 L320,960" stroke="#c8a060" stroke-width="10" fill="none" /><path d="M290,940 L370,930 L360,990 Z" fill="#c8a060" />${cone(340, 980, 100, 300, 70, "#ffcf8a", 0.45)}${glow(340, 990, 200, "amber", 0.7)}</g>
          <g transform="translate(780 1120)">${R(-70, -300, 140, 300, "#e8f4f8", 26, 'opacity="0.85"')}<clipPath id="${P}-oc"><rect x="-66" y="-296" width="132" height="292" rx="22" /></clipPath>
            <g clip-path="url(#${P}-oc)"><rect id="${P}-canfat" x="-70" y="-250" width="140" height="300" fill="#f2d27a" /></g>${R(-70, -300, 140, 300, SH, 26)}${R(-40, -330, 80, 34, "#8a1e3c", 8)}
            <path id="${P}-straw" d="M10,-330 L30,-470 L80,-500" stroke="#e5483a" stroke-width="12" fill="none" stroke-linecap="round" />${T(0, -120, 34, "#8a5a1a", "5 L")}</g></g>`;
    }

    // ── the street outside the clinic at night, close: neon bokeh (P-bokeh), the sign glow at the back, a street lamp P-lamp.
    // Tey close at 540 feet 1400 s 1.25
    function street(slot = "") {
      const sky = grad("ssky", [[0, "#0a0a1c"], [1, "#2a1430"]]);
      const r = rng(55); let bok = ""; for (let i = 0; i < 18; i++) bok += glow(f1(r() * 1080), f1(300 + r() * 700), f1(30 + r() * 70), ["neon", "pink", "amber", "cold"][i % 4], f1(0.25 + r() * 0.35));
      return `<rect width="1080" height="1920" fill="${sky}" />
        <g id="${P}-far"><g id="${P}-bokeh">${bok}</g>${R(200, 560, 680, 170, "#1a1424", 18)}${glow(540, 645, 400, "neon", 0.4)}${T(540, 672, 80, "#ff9cc2", "คลินิกหมอพิม", 700, "middle", 'stroke="#ff3d7f" stroke-width="3" opacity="0.55"')}</g>
        <g id="${P}-mid"><g id="${P}-lamp">${cone(140, 300, 75, 1100, 40, "#ffcf8a", 0.22)}${glow(140, 300, 120, "amber", 0.8)}</g>${R(130, 300, 16, 1100, "#0d0d18")}</g>
        ${slot}<g id="${P}-near">${R(0, 1380, 1080, 540, "#14101c")}${R(0, 1380, 1080, 540, "url(#" + P + "-shadeV)")}<ellipse cx="540" cy="1500" rx="420" ry="60" fill="#ff3d7f" opacity="0.1" /></g>`;
    }

    // ── nurse station at night: counter, computer glow, glass behind with the dark corridor where two red eyes (P-eyes) open.
    // Fon behind the counter at 540 feet 1300 s 1.0
    function station(slot = "") {
      const wall = grad("stw", [[0, "#0e1424"], [1, "#05070e"]]);
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far">${R(120, 300, 840, 640, "#070a14", 10)}<path d="M120,940 L420,620 L660,620 L960,940 Z" fill="#0c1222" />${R(120, 300, 840, 640, "url(#" + P + "-shadeV)", 10)}
          <g id="${P}-eyes" opacity="0">${glow(500, 600, 70, "eye", 0.95)}${glow(580, 600, 70, "eye", 0.95)}<ellipse cx="500" cy="600" rx="12" ry="8" fill="#ff3030" /><ellipse cx="580" cy="600" rx="12" ry="8" fill="#ff3030" /></g>
          ${R(120, 300, 840, 640, "#9fc4e8", 10, 'opacity="0.06"')}<path d="M180,340 L320,340 L200,560 Z" fill="#ffffff" opacity="0.05" /></g>
        <g id="${P}-mid"><g id="${P}-tube">${R(380, 140, 320, 16, "#cfe0ff", 8)}${glow(540, 150, 200, "cold", 0.4)}</g></g>
        ${slot}<g id="${P}-near">${R(60, 1130, 960, 50, "#5a6676", 12)}${R(80, 1180, 920, 740, "#2a3442")}${R(80, 1180, 920, 740, "url(#" + P + "-shadeV)")}
          <g id="${P}-pc">${R(700, 940, 220, 150, "#1a2030", 10)}${R(712, 952, 196, 120, "#7fd6ff", 6, 'opacity="0.8"')}${glow(810, 1010, 200, "cold", 0.5)}${R(790, 1090, 40, 40, "#1a2030")}</g></g>`;
    }
    // ── EP2 · the infectious-waste incinerator, front: furnace mouth with fire (P-fire, P-fireg), a conveyor of red bags (P-belt),
    // chimney smoke (P-smoke). Temperature panel at top right.
    function incinerator(slot = "") {
      const wall = grad("iwall", [[0, "#1a1418"], [1, "#0a080a"]]);
      const bagShape = (x) => `<g transform="translate(${x} 1150)"><path d="M-46,0 Q-60,-70 -30,-96 L30,-96 Q60,-70 46,0 Z" fill="#c8243a" /><path d="M-46,0 Q-60,-70 -30,-96 L30,-96 Q60,-70 46,0 Z" fill="${SH}" /><path d="M-14,-96 L0,-118 L14,-96" fill="#a81c30" /></g>`;
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far"><path d="M820,0 L820,360 L940,360 L940,0 Z" fill="#241c20" /><g id="${P}-smoke">${[0, 1, 2].map((i) => `<circle cx="${880 + i * 30}" cy="${60 - i * 50}" r="${60 + i * 20}" fill="#3a3238" opacity="0.5" />`).join("")}</g>
          ${R(640, 290, 330, 150, "#0a0a10", 14)}${T(805, 340, 30, "#ffb547", "อุณหภูมิเตา")}${T(805, 410, 56, "#ff4636", "1,000°C")}</g>
        <g id="${P}-mid">${R(160, 520, 760, 680, "#3a3036", 30)}${R(160, 520, 760, 680, SH, 30)}${R(250, 640, 580, 420, "#140a08", 30)}
          <g id="${P}-fireg">${glow(540, 900, 420, "amber", 0.9)}${glow(540, 960, 260, "red", 0.8)}</g>
          <g id="${P}-fire">${[[400, 1050, 90], [500, 1060, 120], [600, 1050, 100], [700, 1056, 80]].map(([x, y, h]) => `<path d="M${x - 50},${y} Q${x - 40},${y - h} ${x},${y - h * 1.6} Q${x + 40},${y - h} ${x + 50},${y} Z" fill="#ffb547" opacity="0.9" /><path d="M${x - 26},${y} Q${x - 20},${y - h * 0.6} ${x},${y - h} Q${x + 20},${y - h * 0.6} ${x + 26},${y} Z" fill="#fff1b0" />`).join("")}</g>
          ${R(230, 600, 620, 40, "#5a4a50", 10)}${[300, 540, 780].map((x) => `<circle cx="${x}" cy="620" r="10" fill="#8a7a80" />`).join("")}</g>
        ${slot}<g id="${P}-near">${R(0, 1150, 1080, 40, "#4a4046")}<g id="${P}-belt">${[-300, -60, 180, 420, 660, 900].map(bagShape).join("")}</g>${R(0, 1190, 1080, 730, "#1a1416")}${R(0, 1190, 1080, 730, "url(#" + P + "-shadeV)")}</g>`;
    }
    // ── EP2 · the records room after hours: shelves of binders, a desk lamp P-lamp, a filing cabinet. Fon at 520/1190.
    function records(slot = "") {
      const wall = grad("rwall", [[0, "#1e1a24"], [1, "#0c0a10"]]);
      const cols = ["#c8243a", "#3a8ad0", "#f2c14e", "#5aa06a", "#8a5ab0", "#e88a4a"];
      let binders = ""; for (let row = 0; row < 4; row++) for (let i = 0; i < 12; i++) binders += R(120 + i * 70, 300 + row * 190, 54, 150, cols[(i + row * 2) % 6], 6, `opacity="${row === 3 ? 0.85 : 0.7}"`);
      return `<rect width="1080" height="1920" fill="${wall}" />
        <g id="${P}-far">${R(100, 280, 880, 780, "#2a2230", 10)}${binders}${[0, 1, 2, 3].map((r) => R(100, 452 + r * 190, 880, 14, "#3a3040")).join("")}${R(100, 280, 880, 780, "url(#" + P + "-shadeV)", 10)}</g>
        <g id="${P}-mid"><g id="${P}-lamp"><path d="M860,1120 L880,990 L820,950" stroke="#c8a060" stroke-width="10" fill="none" /><path d="M770,935 L850,925 L840,985 Z" fill="#c8a060" />${cone(810, 975, 110, 420, 80, "#ffcf8a", 0.4)}${glow(810, 985, 260, "amber", 0.7)}</g></g>
        ${slot}<g id="${P}-near">${R(60, 1120, 960, 60, "#3a2e2a", 10)}${R(60, 1180, 960, 740, "#22191a")}${R(60, 1180, 960, 740, "url(#" + P + "-shadeV)")}</g>`;
    }
    // ── EP2 · the back alley in the morning: the clinic's back door, the infectious-waste truck (P-truck), an empty cart. Driver at 300/1190.
    function alley(slot = "") {
      const sky = grad("asky", [[0, "#9fc4dc"], [1, "#e8dccc"]]);
      return `<rect width="1080" height="1920" fill="${sky}" />
        <g id="${P}-far">${R(0, 300, 1080, 900, "#b8aca4")}${R(0, 300, 1080, 900, SH)}${R(80, 560, 220, 600, "#8a7e78")}${R(110, 590, 160, 560, "#6a5e5a")}${R(250, 860, 16, 40, "#c9c0b8", 4)}
          ${R(90, 500, 200, 50, "#c8243a", 8)}${T(190, 536, 28, "#ffffff", "ทางออกขยะ")}${windows(44, 10, 380, 1040, 360, 520, "#e8f0f6")}</g>
        <g id="${P}-mid"><g id="${P}-truck"><g transform="translate(560 1190)">${R(0, -420, 460, 360, "#f4f4f0", 20)}${R(0, -420, 460, 360, SH, 20)}${R(-180, -300, 190, 240, "#e8e8e4", 18)}${R(-160, -280, 130, 100, "#9fc4dc", 10)}
            ${bio(230, -260, 1.4, "#c8243a")}${T(230, -150, 34, "#c8243a", "ขยะติดเชื้อ")}${[-90, 120, 380].map((x) => `<circle cx="${x}" cy="-50" r="52" fill="#2a2a2e" /><circle cx="${x}" cy="-50" r="22" fill="#9a9aa0" />`).join("")}</g></g></g>
        ${slot}<g id="${P}-near">${R(0, 1190, 1080, 730, "#5e5856")}${R(0, 1190, 1080, 730, "url(#" + P + "-shadeV)")}</g>`;
    }
"""
