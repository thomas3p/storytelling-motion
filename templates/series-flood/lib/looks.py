"""Cast of ปอบยุค 5G as flatkit person() / cat() options (front view, flood look). Use in scene JS:
    LOOKS + 'const pim = person({ ...PIM, id: "s03-pim" });'
"""

JS = r"""
    // หมอพิม: the famous surgeon with a Pop bloodline — sleek chignon, long white coat over a wine dress, red lips, beauty mark
    const PIM = { hair: "chignon", hairC: "#15111a", skin: "#f5d6bd", skinD: "#dcae90", brow: "#2a1a14", shirt: "#8a1e3c", coat: "#f7f5f1", coatLong: true,
                  skirt: "#8a1e3c", legC: "#f1cdb2", shoe: "#1c1418", lip: "#c8243a", lash: true, alert: true, smile: true, sw: 140, longSleeve: true, sleeve: "#f7f5f1",
                  extra: ["mole", "earrings", "badge"], badgeC: "#c8243a" };
    // the same doctor in theatre: teal scrubs, cap and mask
    const PIM_OR = { ...PIM, coat: null, shirt: "#3f9aa8", skirt: null, pants: "#3f9aa8", sleeve: "#3f9aa8", longSleeve: false, glove: "#bfe3ea",
                     extra: ["surgcap", "mask"], capC: "#5fb6c2", maskC: "#9fd6e0" };
    // ฝน: the new assistant nurse — ponytail, white uniform and cap, tired-but-trying face
    const FON = { hair: "pony", hairC: "#2a1a14", skin: "#eab48e", skinD: "#c98e68", shirt: "#f4f7fb", skirt: "#e6ecf5", legC: "#f2ece4", shoe: "#ffffff",
                  lash: true, sw: 136, sleeve: "#f4f7fb", extra: ["nursecap", "collar", "pocketpen", "badge"], badgeC: "#3a8ad0" };
    // อาจารย์เต้ย: the new-age exorcist — red yant headband, black hoodie printed with yantra, prayer beads, red sneakers
    const TEY = { hair: "spiky", hairC: "#17131a", skin: "#c8875e", skinD: "#a66a44", brow: "#1a1214", shirt: "#20202a", pants: "#2a2a34", shoe: "#d63a2c",
                  longSleeve: true, sleeve: "#20202a", alert: true, extra: ["headband", "beads", "hood", "zip"],
                  pattern: '<circle cx="17" cy="17" r="7" fill="none" stroke="#f2e6c8" stroke-opacity="0.5" stroke-width="2" /><path d="M10 28 L24 28 M17 4 L17 10" stroke="#f2e6c8" stroke-opacity="0.5" stroke-width="2" />', patW: 34 };
    // the village Pop of the old days (hook): a grandmother in a sarong
    const GRANNY = { hair: "old", hairC: "#dcdcdc", skin: "#d9a98a", skinD: "#b98a6a", brow: "#9a9a9a", shirt: "#6a4a62", skirt: "#3a2a4a", skirtLong: true,
                     legC: "#d9a98a", shoe: "#4a3a2a", alert: true, sw: 138 };
    // clients in the lobby
    const CLIENT_A = { hair: "long", hairC: "#3a2a24", skin: "#f0c8a8", skinD: "#d4a684", shirt: "#e8a4bc", pants: "#4a4a6a", lash: true, extra: ["mask"], maskC: "#f4f4f2" };
    const CLIENT_B = { hair: "bob", hairC: "#1a1418", skin: "#e8b896", skinD: "#c8946e", shirt: "#9fb4d8", pants: "#2b3550", extra: ["glasses"] };
    const CLIENT_C = { hair: "short", hairC: "#22201e", skin: "#d8a07a", skinD: "#b47e5a", shirt: "#5a7a6a", pants: "#2a2a30", extra: ["mask"], maskC: "#cfe8f0" };
    // EP2: a silhouette of the doctor as the night camera sees her (dark body, faint white coat), and the waste-truck driver
    const PIM_SIL = { ...PIM, skin: "#1c1a22", skinD: "#141218", hairC: "#0a080c", brow: "#0a080c", shirt: "#24202a", coat: "#64626e", skirt: "#24202a", legC: "#1c1a22",
                      shoe: "#0a080c", lip: "#3a0a10", sleeve: "#64626e", extra: ["mole"] };
    const DRIVER = { hair: "short", hairC: "#22201e", skin: "#c8875e", skinD: "#a66a44", shirt: "#5a7a8a", pants: "#2e3e4a", shoe: "#2a2420", extra: ["cap", "mask"], capC: "#2e3e4a", maskC: "#e8e8e8" };
    // ไลโป: the clinic's black cat, the only one who knows
    const LIPO = { c: "#2a2630", c2: "#3e3948", plain: true, eye: "#f2c94c", collar: "#c8243a", mouth: "#8a8494" };
"""
