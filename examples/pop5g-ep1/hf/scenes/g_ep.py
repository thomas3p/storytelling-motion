"""Global EP tag (top-left) from the doctor's intro to the end card."""
SCENE = {"title": "ep tag"}


def build(ctx):
    H = ctx.lib.hud
    js = f"""
    pop("#{ctx.sid}-ep", 0.05);
    tl.to("#{ctx.sid}-ep", {{ opacity: 0, duration: 0.25, ease: "sine.in" }}, {ctx.dur - 0.3:.2f});"""
    return ctx.scene("", "", H.ep_tag(f"{ctx.sid}-ep", 1, "บุฟเฟต์ถูกกฎหมาย"), js, bg="transparent", grain=0)
