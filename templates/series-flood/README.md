# Series template: flood look (example cast: ปอบยุค 5G)

Copy with `python tools/new_series.py --root <workspace> --slug <slug> --title "<ชื่อ>"`, then make it yours.

- `series.json` — title, planned episodes, the narrator voice (model, voice, seed, temperature, style_base), look, motion, palette, render flags
- `lib/hud.py` — `KIT = "flat"` (scenes use tools/flatkit) + overlays: `ep_tag`, `card`, `stat`, `chip`, `bubble`, `receipt`, `appt`, `series_line`, `title`
- `lib/looks.py` — characters as `person()` options in a JS string: PIM (doctor), PIM_OR (theatre), PIM_SIL (night-camera silhouette), FON (nurse), TEY (new-age exorcist), GRANNY (village Pop), CLIENT_A/B/C, DRIVER, LIPO (black cat). See `examples/characters/characters.html`.
- `lib/sets.py` — places as JS functions with far/mid/near parallax layers and a `slot`: village, clinicExt (night/day), lobby, oroom, corridor, wasteRoom, office, street, station, incinerator, records, alley

Add a character: copy a look, change hair/colours/extras (options in references/flatkit.md), rebuild the sheet with `python examples/characters/build_sheet.py --png` to see it.
