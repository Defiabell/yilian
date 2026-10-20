#!/usr/bin/env python3
"""Render public/og.png (1200x630) for link previews.

Palette and type follow public/index.html (dark theme): bg #111419, fg #eef0f3,
muted #99a2ad, accent #ff7b47; CJK in Hiragino Sans GB (PingFang fallback in
CSS), Latin in Barlow Condensed (site display font), Arial Narrow as fallback.

Run from the repo root: python3 scripts/og.py
Set BARLOW_TTF to a BarlowCondensed-Bold.ttf path to use the real display font.
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "og.png"

W, H = 1200, 630
BG, FG, MUTED, ACCENT = "#111419", "#eef0f3", "#99a2ad", "#ff7b47"
MARGIN = 84

CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"  # index 0 = W3, 2 = W6
TITLE = "一练·四练上下肢计划"  # full-width dot already carries its own spacing
DESC = "每周四练的上下肢分化训练计划：动作示意图、组数次数、要点、勾选和组间计时。"
DOMAIN = "yilian.defiabell.com"


def latin_font(size: int) -> ImageFont.FreeTypeFont:
    for path in (
        os.environ.get("BARLOW_TTF", ""),
        "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf",
    ):
        if path and Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    """Greedy per-character wrap (CJK has no spaces); never breaks on a leading
    punctuation mark."""
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=font) <= max_w or not cur:
            cur += ch
        elif ch in "，。：；、！？）》":
            cur += ch  # keep closing punctuation on the line it belongs to
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(CJK, 88, index=2)
    desc_font = ImageFont.truetype(CJK, 36, index=0)
    domain_font = latin_font(34)

    # accent tick, same role as the accent bar in the app header
    d.rectangle([MARGIN, 112, MARGIN + 56, 112 + 8], fill=ACCENT)

    y = 150
    d.text((MARGIN - 4, y), TITLE, font=title_font, fill=FG)
    y += 88 + 44

    for line in wrap(d, DESC, desc_font, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=desc_font, fill=MUTED)
        y += 36 + 18

    # domain, small, bottom-left, tracked like the display font in the UI
    x = MARGIN
    spacing = 2
    for ch in DOMAIN:
        d.text((x, H - MARGIN - 34), ch, font=domain_font, fill=ACCENT)
        x += d.textlength(ch, font=domain_font) + spacing

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
