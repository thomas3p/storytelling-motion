"""Cast of 60°C รุ่งอรุณเดือด as flatkit person() options (front view, flood look). Use in scene JS:
    LOOKS + 'const ch = person({ ...CHAIN, id: "s04-ch" });'  then  sweat(ch, "s04-ch") for the heat look.
"""

JS = r"""
    // เชน: the condo's maintenance technician — short black hair, tanned, blue work shirt with a name badge, dark work trousers,
    // brown boots, a tool belt (drawn by toolbelt()), tired-but-steady face
    const CHAIN = { hair: "short", hairC: "#17141a", skin: "#d39a72", skinD: "#b07a54", brow: "#1e1612", shirt: "#2f6a9a", pants: "#26313f", shoe: "#5a3e2a",
                    sleeve: "#2f6a9a", sw: 150, extra: ["badge", "pocketpen", "collar"], badgeC: "#f2b83a" };
    // the same man later in the heat: skin flushed red, shirt dark with sweat
    const CHAIN_HOT = { ...CHAIN, skin: "#e28a6a", skinD: "#c06a4c", shirt: "#24557e", sleeve: "#24557e" };
    // the TV news anchor (breaking news)
    const NEWS = { hair: "bob", hairC: "#1a1418", skin: "#f0c8a8", skinD: "#d4a684", shirt: "#c8243a", coat: "#1b2440", sleeve: "#1b2440", longSleeve: true,
                   lip: "#b8323a", lash: true, alert: true, sw: 140, extra: ["earrings"] };

    // tool belt across the hips of a person() result r (local coords, origin = between the feet)
    const toolbelt = (r) => {
      const y = r.hipY - 6, w = 160;
      return `<rect x="${f1(-w / 2)}" y="${f1(y - 4)}" width="${w}" height="22" rx="8" fill="#5a3e2a" />`
        + `<rect x="${f1(-w / 2 + 6)}" y="${f1(y + 10)}" width="44" height="54" rx="8" fill="#7a5638" /><rect x="${f1(w / 2 - 50)}" y="${f1(y + 10)}" width="44" height="54" rx="8" fill="#7a5638" />`
        + `<rect x="${f1(-w / 2 + 16)}" y="${f1(y - 16)}" width="8" height="30" rx="3" fill="#b8bec8" /><rect x="${f1(w / 2 - 34)}" y="${f1(y - 22)}" width="10" height="36" rx="3" fill="#e5483a" />`
        + `<rect x="-14" y="${f1(y)}" width="28" height="14" rx="3" fill="#c9a24a" />`;
    };
    // sweat drops on a face; returns an SVG group "<id>-sw" (animate its children's y/opacity in the scene)
    const sweat = (r, id, n = 4) => {
      const hy = r.hy, hs = r.hs || 1, spots = [[-58, -20], [56, -6], [-30, -50], [34, -46], [62, 26], [-62, 30]];
      return `<g id="${id}-sw">${spots.slice(0, n).map(([x, y], i) => `<path class="${id}-drop" d="M${f1(x * hs)},${f1(hy + y * hs - 10)} q-7,12 0,18 q7,-6 0,-18 Z" fill="#bfe6ff" opacity="0.9" />`).join("")}</g>`;
    };
"""
