"""Compose cut-out flowers into arrangements for the site.
usage: python -I compose.py <cut_dir> <out_dir>"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

cut, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)


def load(name):
    return Image.open(cut / f"{name}.png").convert("RGBA")


def deepen(im, g=0.72, b=0.85, v=0.9):
    """Pull the orange-red rose toward the wedding red."""
    a = np.asarray(im).astype(float)
    a[..., 0] *= v
    a[..., 1] *= g * v
    a[..., 2] *= b * v
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def shadow(im, blur=10, op=0.22, off=(6, 8)):
    """Soft drop shadow so overlapping flowers have depth."""
    a = im.split()[3].point(lambda v: int(v * op))
    sh = Image.new("RGBA", im.size, (60, 25, 20, 0))
    sh.putalpha(a)
    return sh.filter(ImageFilter.GaussianBlur(blur)), off


def place(canvas, im, x, y, scale=1.0, rot=0.0, flip=False, vflip=False, shade=True):
    im = im.copy()
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if vflip:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    px, py = int(x - im.width / 2), int(y - im.height / 2)
    if shade:
        sh, (dx, dy) = shadow(im)
        canvas.alpha_composite(sh, (max(0, px + dx), max(0, py + dy))) if px + dx >= 0 and py + dy >= 0 else canvas.paste(sh, (px + dx, py + dy), sh)
    if px >= 0 and py >= 0:
        canvas.alpha_composite(im, (px, py))
    else:
        canvas.paste(im, (px, py), im) if False else _composite_clip(canvas, im, px, py)


def _composite_clip(canvas, im, px, py):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(im, (px, py), im)
    canvas.alpha_composite(layer)


def save(canvas, name, size):
    bbox = canvas.getbbox()
    canvas = canvas.crop(bbox)
    canvas.thumbnail(size, Image.LANCZOS)
    canvas.save(out / f"{name}.webp", "WEBP", quality=82, method=6)
    canvas.save(out / f"{name}-preview.png")
    print(name, canvas.size)


def fade(im, left=0, right=0, top=0, bottom=0):
    """Fade alpha toward edges where the source photo cropped the flowers."""
    a = np.asarray(im).astype(float)
    h, w = a.shape[:2]
    m = np.ones((h, w))
    xs, ys = np.arange(w)[None, :], np.arange(h)[:, None]
    if left: m *= np.clip(xs / left, 0, 1)
    if right: m *= np.clip((w - 1 - xs) / right, 0, 1)
    if top: m *= np.clip(ys / top, 0, 1)
    if bottom: m *= np.clip((h - 1 - ys) / bottom, 0, 1)
    a[..., 3] *= m
    return Image.fromarray(a.astype(np.uint8), "RGBA")


rose = deepen(load("rose_head"))
stem = load("rose_stem")
lying = load("rose_lying")
bud = stem.crop((0, 0, stem.width, int(stem.height * 0.42)))  # rose bud + leaves
g1 = load("gyps_dark1")
sprigs = fade(g1.crop((330, 0, g1.width, 470)), left=90, bottom=140)  # crisp top branches only
g2 = load("gyps_dark2")
mound = fade(g2, bottom=170, left=60, right=60)  # dense, sharp cloud; flat table edge faded

# --- A: corner bouquet (anchored at the top-left corner of the canvas) ---
c = Image.new("RGBA", (1400, 1400), (0, 0, 0, 0))
place(c, mound, 360, 330, 0.85, -35, shade=False)
place(c, mound, 260, 640, 0.6, -70, shade=False)
place(c, sprigs, 720, 260, 0.85, -15, shade=False)
place(c, sprigs, 240, 880, 0.7, -110, shade=False)
place(c, lying, 330, 200, 0.68, -150, flip=True)
place(c, bud, 760, 210, 0.8, -62)
place(c, rose, 210, 250, 0.46, 10)
place(c, rose, 470, 440, 0.32, -20)
place(c, lying, 150, 560, 0.48, 118)
place(c, bud, 200, 820, 0.6, 175)
save(c, "flowers-corner", (900, 900))

# --- B: horizontal garland (divider / phone header) ---
g = Image.new("RGBA", (2000, 900), (0, 0, 0, 0))
place(g, mound, 700, 420, 0.95, 4, shade=False)
place(g, mound, 1300, 430, 0.85, -5, flip=True, shade=False)
place(g, sprigs, 260, 400, 0.6, 60, shade=False)
place(g, sprigs, 1740, 400, 0.6, -60, flip=True, shade=False)
place(g, lying, 600, 560, 0.55, 14, flip=True)
place(g, lying, 1400, 575, 0.5, -16)
place(g, bud, 330, 500, 0.62, 72)
place(g, bud, 1670, 500, 0.62, -72)
place(g, rose, 1000, 560, 0.5, 0)
save(g, "flowers-garland", (1400, 700))

# --- C: small sprig that peeks in from the page edge ---
s = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
place(s, sprigs, 470, 430, 0.95, -20, shade=False)
place(s, mound, 330, 640, 0.45, -40, shade=False)
place(s, bud, 640, 380, 0.75, -35)
place(s, rose, 300, 660, 0.3, 0)
save(s, "flowers-sprig", (600, 600))
