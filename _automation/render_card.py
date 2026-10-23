#!/usr/bin/env python3
"""Render a Research Radar title card (STYLE_GUIDE §9).

1200x630 OG card, fixed brand palette, one typeface, no generative imagery.
Requires Pillow:  pip install pillow

Usage: python3 render_card.py <YYYY-MM-DD> "<theme line>"
Writes ../images/radar/<date>-card.png (published path: /images/radar/...).
"""
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not installed: pip install pillow", file=sys.stderr)
    raise SystemExit(1)

W, H = 1200, 630
BG = (15, 23, 42)       # slate-900 brand base
FG = (241, 245, 249)    # near-white
ACCENT = (249, 115, 22) # orange accent (matches site award chips)
MUTED = (148, 163, 184)
OUT_DIR = Path(__file__).resolve().parents[1] / "images" / "radar"


def _font(size: int, bold: bool = False):
    # Fall back to Pillow's default if no TTF is found; keep it dependency-light.
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
        "/Library/Fonts/Arial%s.ttf" % (" Bold" if bold else ""),
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def render(date_str: str, theme: str, noun: str = "paper") -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 12, H], fill=ACCENT)            # left accent bar
    d.text((80, 90), "RESEARCH RADAR", font=_font(34, True), fill=ACCENT)
    d.text((80, 150), f"One {noun},", font=_font(52, True), fill=FG)
    d.text((80, 215), "explained in depth.", font=_font(52, True), fill=FG)

    # Paper short name (wrap to two lines if long).
    theme = theme.strip() or "today's paper"
    line1, line2 = theme[:46], theme[46:92]
    d.text((80, 330), line1, font=_font(34, True), fill=MUTED)
    if line2:
        d.text((80, 378), line2, font=_font(34, True), fill=MUTED)

    d.text((80, H - 90), date_str, font=_font(30, True), fill=FG)
    d.text((W - 360, H - 90), "hyeonjongjang.github.io", font=_font(26), fill=MUTED)

    out = OUT_DIR / f"{date_str}-card.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: render_card.py <YYYY-MM-DD> [theme] [noun]", file=sys.stderr)
        raise SystemExit(2)
    render(sys.argv[1],
           sys.argv[2] if len(sys.argv) > 2 else "",
           sys.argv[3] if len(sys.argv) > 3 else "paper")
