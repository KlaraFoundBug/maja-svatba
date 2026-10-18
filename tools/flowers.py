#!/usr/bin/env python3
"""Builds the watercolour flower arrangements in img/flowers/.

Roses: free watercolour rose clipart from Pixabay (Pixabay Content License,
free for personal & commercial use, no attribution required):
https://pixabay.com/illustrations/rose-bloom-petals-flower-plant-9551838/
Baby's breath: painted procedurally below (thin sage stems + soft white florets).

usage: python3 tools/flowers.py <path to rose-9551838.png>   (needs Pillow + numpy)
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "img" / "flowers"
SS = 2
STEM = (132, 152, 116, 255)
SHADE = (172, 178, 186)


def pieces(sheet_path):
    sheet = Image.open(sheet_path).convert("RGBA")

    def cut(box, clear=()):
        p = sheet.crop(box)
        d = ImageDraw.Draw(p)
        for c in clear:  # remove bits of neighbouring motifs
            d.rectangle([c[0] - box[0], c[1] - box[1], c[2] - box[0], c[3] - box[1]], fill=(0, 0, 0, 0))
        return keep_main_parts(p)

    return {
        "stem_rose": cut((20, 20, 925, 1240), clear=[(745, 20, 925, 470), (645, 770, 925, 1240)]),
        "rose": cut((640, 760, 1262, 1262)),
        "bud": cut((740, 30, 1240, 770), clear=[(740, 470, 940, 770)]),
    }


def keep_main_parts(im, min_share=0.04):
    """Drop small stray scraps left over from cropping (keeps big connected parts)."""
    from collections import deque
    n = 200
    small = np.asarray(im.split()[3].resize((n, n)).filter(ImageFilter.MaxFilter(3))) > 25
    label = np.zeros((n, n), int)
    sizes = [0]
    for y in range(n):
        for x in range(n):
            if small[y, x] and not label[y, x]:
                k = len(sizes); q = deque([(y, x)]); label[y, x] = k; cnt = 0
                while q:
                    cy, cx = q.popleft(); cnt += 1
                    for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                        if 0 <= ny < n and 0 <= nx < n and small[ny, nx] and not label[ny, nx]:
                            label[ny, nx] = k; q.append((ny, nx))
                sizes.append(cnt)
    keep = np.isin(label, [i for i, c in enumerate(sizes) if i and c >= max(sizes) * min_share])
    mask = Image.fromarray((keep * 255).astype(np.uint8)).resize(im.size, Image.NEAREST).filter(ImageFilter.MaxFilter(5))
    a = np.minimum(np.asarray(im.split()[3]), np.asarray(mask))
    im = im.copy(); im.putalpha(Image.fromarray(a))
    return im.crop(im.getbbox())


def gypsophila(length, ang, seed, depth=5, spread=0.55):
    """Paint one airy spray of baby's breath on its own transparent layer."""
    rng = np.random.default_rng(seed)
    w = h = int(length * 3.2)
    ox, oy = w / 2, h / 2
    lines, florets = [], []

    def branch(x0, y0, L, a, d):
        x1, y1 = x0 + math.cos(a) * L, y0 + math.sin(a) * L
        lines.append(((x0, y0), (x1, y1), max(1.0, d * 0.7)))
        if d == 0:
            florets.append((x1, y1))
            return
        for _ in range(int(rng.integers(2, 4))):
            branch(x1, y1, L * rng.uniform(0.52, 0.7), a + rng.uniform(-spread, spread), d - 1)
        if rng.random() < 0.45:
            florets.append((x1, y1))

    branch(ox, oy, length * 0.55, ang, depth)
    big = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    for a, b, wd in lines:
        d.line([(a[0] * SS, a[1] * SS), (b[0] * SS, b[1] * SS)], fill=STEM, width=max(1, int(wd * SS)))
    dots = []
    for fx, fy in florets:
        for _ in range(int(rng.integers(4, 8))):
            dots.append((fx + rng.normal(0, 4), fy + rng.normal(0, 4), rng.uniform(2.2, 3.8)))
    shade = Image.new("L", big.size, 0)
    ds = ImageDraw.Draw(shade)
    petals = Image.new("L", big.size, 0)
    dp = ImageDraw.Draw(petals)
    for x, y, r in dots:  # soft grey-blue edge so white florets read on cream paper
        ds.ellipse([(x - r * 1.3) * SS, (y - r * 1.3) * SS, (x + r * 1.3) * SS, (y + r * 1.3) * SS], fill=190)
        dp.ellipse([(x - r * 0.95 + 0.6) * SS, (y - r * 0.95 - 0.6) * SS, (x + r * 0.95 + 0.6) * SS, (y + r * 0.95 - 0.6) * SS], fill=255)
    shade = shade.filter(ImageFilter.GaussianBlur(0.9 * SS))
    petals = petals.filter(ImageFilter.GaussianBlur(0.4 * SS))
    big.alpha_composite(Image.merge("RGBA", (*[Image.new("L", big.size, c) for c in SHADE], shade)))
    big.alpha_composite(Image.merge("RGBA", (*[Image.new("L", big.size, c) for c in (255, 255, 252)], petals)))
    im = big.resize((w, h), Image.LANCZOS)
    return im.crop(im.getbbox())


def place(canvas, im, x, y, scale=1.0, rot=0.0, flip=False):
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(im, (int(x - im.width / 2), int(y - im.height / 2)), im)
    canvas.alpha_composite(layer)


def save(canvas, name, size):
    im = canvas.crop(canvas.getbbox())
    im.thumbnail(size, Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / f"{name}.webp", "WEBP", quality=86, method=6)
    print(name, im.size)


def main(sheet_path):
    p = pieces(sheet_path)
    rose, bud, stem_rose = p["rose"], p["bud"], p["stem_rose"]

    # A: loose corner spray, anchored top-left
    c = Image.new("RGBA", (1100, 1100), (0, 0, 0, 0))
    place(c, gypsophila(300, -0.15, 1), 470, 170)
    place(c, gypsophila(260, 0.35, 2), 380, 250)
    place(c, gypsophila(280, 1.35, 3), 150, 470)
    place(c, gypsophila(240, 1.0, 4), 250, 380)
    place(c, bud, 560, 240, 0.42, -62)
    place(c, bud, 230, 600, 0.36, 160, flip=True)
    place(c, rose, 210, 200, 0.6, 12)
    save(c, "flowers-corner", (800, 800))

    # B: airy horizontal garland (phones/tablets + footer)
    g = Image.new("RGBA", (1800, 700), (0, 0, 0, 0))
    place(g, gypsophila(300, math.pi - 0.1, 5), 640, 330)
    place(g, gypsophila(260, math.pi + 0.45, 6), 700, 300)
    place(g, gypsophila(300, 0.1, 7), 1160, 330)
    place(g, gypsophila(260, -0.45, 8), 1100, 300)
    place(g, bud, 520, 380, 0.38, 100, flip=True)
    place(g, bud, 1280, 380, 0.38, -100)
    place(g, rose, 900, 360, 0.55, 0)
    save(g, "flowers-garland", (1400, 560))

    # C: single stem with baby's breath, for accents
    s = Image.new("RGBA", (1100, 1400), (0, 0, 0, 0))
    place(s, gypsophila(320, -1.2, 9), 600, 600)
    place(s, gypsophila(260, -1.9, 10), 450, 640)
    place(s, stem_rose, 550, 700, 0.8, 0)
    save(s, "flowers-sprig", (600, 760))


if __name__ == "__main__":
    main(sys.argv[1])
