"""Episode-wide pieces for ปอบยุค 5G ตอนที่ 2: the look of Fon's hidden phone camera (green night tint, scanlines, REC + timestamp)."""

FOOT_CSS = """
    .ft-ui { position: absolute; left: 60px; right: 60px; top: 262px; z-index: 17; display: flex; justify-content: space-between; align-items: center;
             font-family: "Mitr", sans-serif; font-weight: 600; font-size: 36px; color: #e8ffe8; text-shadow: 0 2px 6px rgba(0, 0, 0, 0.8); background: rgba(0, 12, 4, 0.72); padding: 6px 20px 8px; border-radius: 14px; }
    .ft-ui b { display: inline-flex; align-items: center; gap: 12px; }
    .ft-ui b::before { content: ""; width: 22px; height: 22px; border-radius: 50%; background: #ff3030; box-shadow: 0 0 14px #ff3030; }"""


def foot_svg(p):
    """Green night-vision tint (colour blend) + scanlines + a soft dark edge, drawn over the whole frame."""
    lines = "".join(f'<rect y="{y}" width="1080" height="2" fill="#000" opacity="0.22" />' for y in range(0, 1920, 7))
    return (f'<rect width="1080" height="1920" fill="#7dffa8" style="mix-blend-mode: color" opacity="0.85" />'
            f'<rect width="1080" height="1920" fill="#0a2a14" opacity="0.18" />{lines}')


def foot_ui(id, stamp):
    return f'    <div id="{id}" class="ft-ui"><b>REC</b><span id="{id}-ts">{stamp}</span></div>'
