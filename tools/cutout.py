"""Cut flowers out of studio photos -> transparent PNGs.
usage: python -I cutout.py <src_dir> <out_dir>
Roses on light backgrounds are keyed by colour saturation (kills grey shadows);
gypsophila on black backgrounds by brightness."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def save(rgb, alpha, name, maxside=1000):
    a8 = (alpha * 255).astype(np.uint8)
    img = Image.fromarray(np.dstack([rgb.astype(np.uint8), a8]), "RGBA")
    bbox = Image.fromarray(a8).point(lambda v: 255 if v > 8 else 0).getbbox()
    img = img.crop(bbox)
    img.thumbnail((maxside, maxside), Image.LANCZOS)
    img.save(out / f"{name}.png")
    print(name, img.size)


def light_key(name, lo=22, hi=60, crop=None):
    im = np.asarray(Image.open(src / f"{name}.jpg").convert("RGB")).astype(float)
    if crop:
        im = im[crop[1]:crop[3], crop[0]:crop[2]]
    chroma = im.max(2) - im.min(2)
    dark = 255 - im.mean(2)
    a = np.maximum(smooth(chroma, lo, hi), smooth(dark, 150, 200))
    # remove the light background cast from semi-transparent edge pixels
    bg = np.array([238.0, 238.0, 240.0])
    ae = np.maximum(a, 1e-3)[..., None]
    rgb = np.clip((im - (1 - ae) * bg) / ae, 0, 255)
    save(rgb, a, name)


def dark_key(name, crop=None):
    im = np.asarray(Image.open(src / f"{name}.jpg").convert("RGB")).astype(float)
    if crop:
        im = im[crop[1]:crop[3], crop[0]:crop[2]]
    lum = im @ np.array([0.299, 0.587, 0.114])
    chroma = im.max(2) - im.min(2)
    a = np.maximum(smooth(lum, 48, 118), smooth(chroma, 20, 45) * smooth(lum, 35, 70))
    ae = np.maximum(a, 1e-3)[..., None]
    rgb = np.clip(im / ae, 0, 255)  # un-premultiply against black
    # lift the shadowed petals so the flowers read as white, keep a little shading
    rgb = np.clip(rgb * 1.18 + 12, 0, 255)
    save(rgb, a, name)


light_key("rose_head", lo=40, hi=75)
light_key("rose_stem")
light_key("rose_lying")
dark_key("gyps_dark1")
dark_key("gyps_dark2", crop=(0, 0, 1600, 800))
