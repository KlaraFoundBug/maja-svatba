#!/usr/bin/env python3
"""Builds img/og.jpg – the preview picture shown when the link is shared (WhatsApp, Messenger, …).

usage: python3 tools/og_image.py <fonts_dir>
fonts_dir must contain BodoniModa.ttf, BodoniModa-Italic.ttf and Lato-Bold.ttf
(free from https://github.com/google/fonts, OFL licence). Needs Pillow.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

fonts = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "img" / "og.jpg"
W, H = 1200, 630
PAPER, TINT, RED, INK, MUTED = (255, 253, 251), (248, 236, 234), (179, 33, 30), (42, 33, 30), (116, 102, 95)


def font(name, size, opsz=None, wght=400):
    f = ImageFont.truetype(str(fonts / name), size)
    try:  # variable font axes (optical size + weight)
        axes = f.get_variation_axes()
        f.set_variation_by_axes([opsz or 96 if a["name"] in (b"Optical size", "Optical size") else wght for a in axes])
    except Exception:
        pass
    return f


im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)
d.rectangle([0, H - 120, W, H], fill=TINT)

amp = font("BodoniModa-Italic.ttf", 470)
d.text((W / 2, 300), "&", font=amp, fill=(242, 214, 211), anchor="mm")

label = font("Lato-Bold.ttf", 22)
d.text((W / 2, 86), "B E R E M E   S E", font=label, fill=RED, anchor="mm")

names = font("BodoniModa.ttf", 128)
d.text((W / 2, 230), "Mája", font=names, fill=INK, anchor="mm")
d.text((W / 2, 370), "Míša", font=names, fill=INK, anchor="mm")

date = font("BodoniModa.ttf", 46)
d.text((W / 2, H - 60), "5 · 6 · 2027   ·   Stodola Plástovice", font=date, fill=RED, anchor="mm")

im.save(OUT, "JPEG", quality=88)
print("wrote", OUT)
