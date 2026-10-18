#!/usr/bin/env python3
"""Generates the dummy SVG artwork for the site (florals, invite, placeholder photos).

Run from the repo root:  python3 tools/generate_art.py
Replace files in img/ with real photos / a scan of the real invite whenever you have them.
"""
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"

RED = "#B3211E"
RED_DARK = "#8E1A1A"
RED_DEEP = "#5C1A1E"
RED_LIGHT = "#C93A33"
SAGE = "#8FB27A"
SAGE_DARK = "#1E4A33"
IVORY = "#F6F1E9"
INK = "#2B2323"

random.seed(7)


def petals(n, d, fill, offset=0.0):
    return "".join(
        f'<path d="{d}" fill="{fill}" transform="rotate({offset + i * 360 / n:.1f})"/>' for i in range(n)
    )


DEFS = f"""
<defs>
  <g id="rose">
    {petals(5, "M0 0 C -27 -5 -31 -36 -6 -41 C 7 -44 15 -30 0 0Z", RED_DARK)}
    {petals(5, "M0 0 C -22 -4 -25 -30 -5 -34 C 6 -36 12 -25 0 0Z", RED, 36)}
    {petals(5, "M0 0 C -16 -3 -18 -22 -4 -25 C 4 -26 9 -18 0 0Z", RED_LIGHT, 12)}
    <circle r="11" fill="{RED_DARK}"/>
    <path d="M-7 -1 C -7 -10 7 -10 7 -1 C 7 6 -4 7 -4 1 C -4 -3 1 -4 2 -1" stroke="{RED_DEEP}" stroke-width="1.4" fill="none" stroke-linecap="round"/>
    <path d="M-20 -14 C -14 -22 -4 -24 4 -22" stroke="#fff" stroke-opacity=".18" stroke-width="1.2" fill="none"/>
    <path d="M14 10 C 18 4 18 -4 15 -9" stroke="#fff" stroke-opacity=".14" stroke-width="1.2" fill="none"/>
  </g>
  <g id="bud">
    <path d="M0 0 C -9 -8 -8 -24 0 -30 C 8 -24 9 -8 0 0Z" fill="{RED}"/>
    <path d="M0 -4 C -4 -12 -2 -22 2 -27" stroke="{RED_DEEP}" stroke-width="1" fill="none"/>
    <path d="M0 2 C -10 -2 -12 -10 -10 -16 C -6 -8 -3 -4 0 -2Z M0 2 C 10 -2 12 -10 10 -16 C 6 -8 3 -4 0 -2Z" fill="{SAGE_DARK}"/>
  </g>
  <g id="leaf">
    <path d="M0 0 C 12 -11 30 -11 44 0 C 30 10 12 10 0 0Z" fill="{SAGE_DARK}"/>
    <path d="M3 0 L40 0" stroke="#163826" stroke-width=".9"/>
  </g>
  <g id="bb">
    <path d="M0 0 L-10 -18 M0 0 L4 -24 M0 0 L15 -14 M-10 -18 L-17 -27 M-10 -18 L-6 -30 M4 -24 L1 -35 M4 -24 L11 -33 M15 -14 L24 -21 M15 -14 L22 -6" stroke="{SAGE}" stroke-width=".8" fill="none"/>
    <g fill="#fff" stroke="#C9BFAE" stroke-width=".6">
      {"".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [
        (-17, -27, 2.6), (-20, -24, 1.8), (-15, -31, 1.7), (-6, -30, 2.6), (-3, -33, 1.7), (-9, -33, 1.6),
        (1, -35, 2.6), (-2, -38, 1.7), (4, -39, 1.6), (11, -33, 2.6), (14, -35, 1.7), (10, -37, 1.5),
        (24, -21, 2.6), (27, -23, 1.7), (25, -17, 1.6), (22, -6, 2.4), (25, -4, 1.6), (-10, -18, 1.6)])}
    </g>
  </g>
</defs>"""


def svg(w, h, body, extra_defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}">{DEFS}{extra_defs}{body}</svg>\n'
    )


def use(ref, x, y, s=1.0, r=0.0):
    return f'<use href="#{ref}" xlink:href="#{ref}" transform="translate({x} {y}) rotate({r}) scale({s})"/>'


def bouquet_corner():
    """Top-left corner arrangement, 420x420."""
    stems = f'<path d="M-10 40 C 80 70 180 40 300 10 M20 -10 C 50 90 40 200 10 330 M60 60 C 140 120 200 160 250 230" stroke="{SAGE}" stroke-width="1.6" fill="none"/>'
    parts = [
        stems,
        use("bb", 300, 40, 1.5, 70), use("bb", 255, 95, 1.3, 120), use("bb", 250, 230, 1.4, 150),
        use("bb", 30, 330, 1.4, 200), use("bb", 105, 250, 1.3, 170), use("bb", 200, 160, 1.1, 130),
        use("bb", 360, 15, 1.1, 80), use("bb", 0, 380, 1.1, 220),
        use("leaf", 150, 115, 1.2, 25), use("leaf", 115, 150, 1.1, 70), use("leaf", 205, 60, 1.0, -15),
        use("leaf", 50, 210, 1.1, 95), use("leaf", 230, 30, .9, 10), use("leaf", 160, 190, .9, 45),
        use("bud", 262, 32, 1.0, 70), use("bud", 30, 280, 1.0, 200), use("bud", 185, 175, .8, 135),
        use("rose", 175, 58, 1.0, 20), use("rose", 60, 185, 1.0, -30), use("rose", 92, 88, 1.55, 0),
    ]
    return svg(420, 420, "".join(parts))


def divider():
    parts = [
        f'<path d="M20 30 L120 30 M180 30 L280 30" stroke="{SAGE}" stroke-width="1"/>',
        use("bb", 120, 30, .9, -80), use("bb", 180, 30, .9, 80),
        use("leaf", 150, 30, .55, 200), use("leaf", 150, 30, .55, -20),
        use("rose", 150, 30, .55, 0),
    ]
    return svg(300, 60, "".join(parts))


def sprig():
    """Single vertical baby's breath sprig with a bud, for subtle accents."""
    parts = [
        f'<path d="M60 230 C 58 170 64 120 60 40" stroke="{SAGE}" stroke-width="1.2" fill="none"/>',
        use("bb", 60, 60, 1.4, 0), use("bb", 60, 120, 1.2, -40), use("bb", 60, 160, 1.1, 50),
        use("leaf", 60, 190, .7, -140), use("leaf", 61, 150, .6, -30),
    ]
    return svg(120, 240, "".join(parts))


def invite():
    """Dummy invitation card 600x840 — replace with a photo/scan of the real one."""
    W, H = 600, 840
    serif = "Didot, 'Bodoni 72', 'Playfair Display', Georgia, serif"
    script = "'Snell Roundhand', 'Pinyon Script', 'Apple Chancery', cursive"
    extra = """
<defs>
  <filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/>
    <feColorMatrix values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .45  0 0 0 .06 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
</defs>"""
    body = f"""
<rect width="{W}" height="{H}" fill="#FBF8F2"/>
<rect width="{W}" height="{H}" filter="url(#paper)"/>
<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="{RED}" stroke-width="1.2"/>
<rect x="30" y="30" width="{W-60}" height="{H-60}" fill="none" stroke="{RED}" stroke-width=".5"/>
<g transform="translate(300 118)">
  <path d="M-150 10 C -80 0 -40 4 0 10 C 40 4 80 0 150 10" stroke="{SAGE}" stroke-width="1.2" fill="none"/>
  {use("bb", -95, 6, 1.3, -70)}{use("bb", 95, 6, 1.3, 70)}{use("bb", -140, 10, 1.0, -85)}{use("bb", 140, 10, 1.0, 85)}
  {use("leaf", -30, 6, .8, 190)}{use("leaf", 30, 6, .8, -10)}{use("leaf", -10, 18, .6, 140)}
  {use("bud", -55, 4, .8, -60)}{use("bud", 55, 4, .8, 60)}
  {use("rose", 0, 0, 1.15, 0)}
</g>
<g font-family="{serif}" fill="{INK}" text-anchor="middle">
  <text x="300" y="232" font-size="15" letter-spacing="5">SPOLU S RODIČI</text>
  <text x="300" y="256" font-size="15" letter-spacing="5">VÁS SRDEČNĚ ZVOU</text>
  <text x="300" y="350" font-size="64" letter-spacing="6">MAJA</text>
  <text x="300" y="412" font-family="{script}" font-size="56" fill="{RED}">&amp;</text>
  <text x="300" y="480" font-size="64" letter-spacing="6">JAKUB</text>
  <text x="300" y="540" font-size="15" letter-spacing="5">NA SVŮJ SVATEBNÍ DEN</text>
  <line x1="180" y1="575" x2="420" y2="575" stroke="{RED}" stroke-width=".8"/>
  <text x="300" y="612" font-size="26" letter-spacing="8">6 · 7 · 2027</text>
  <line x1="180" y1="632" x2="420" y2="632" stroke="{RED}" stroke-width=".8"/>
  <text x="300" y="672" font-size="15" letter-spacing="4">OBŘAD VE 14:00</text>
  <text x="300" y="700" font-size="17" font-style="italic">Zámecký statek Lipová (dummy místo)</text>
  <text x="300" y="770" font-family="{script}" font-size="26" fill="{RED}">Těšíme se na vás</text>
</g>"""
    return svg(W, H, body, extra)


PHOTOS = [
    # (filename, w, h, caption, gradient from, to)
    ("maja-detstvi.svg", 800, 1000, "Malá Maja, cca 1998", "#d9c4b0", "#8f7766"),
    ("jakub-detstvi.svg", 800, 1000, "Malý Jakub, cca 1997", "#cdbfae", "#6f665c"),
    ("seznameni.svg", 1200, 800, "Kde se to všechno stalo", "#d8c8bb", "#7c6a5f"),
    ("spolecny-zivot.svg", 1200, 800, "Spolu na cestách", "#e2d3c3", "#8a7363"),
    ("zasnuby.svg", 800, 1000, "Zásnuby", "#e6d2c8", "#9b6f68"),
    ("hero.svg", 1600, 1000, "Úvodní fotka páru", "#c9b8a8", "#5f5148"),
    ("galerie-1.svg", 800, 1000, "Momentka 1", "#e3d6c8", "#8d7a6b"),
    ("galerie-2.svg", 800, 800, "Momentka 2", "#d7c9bd", "#7b6c62"),
    ("galerie-3.svg", 800, 1000, "Momentka 3", "#e4cfc6", "#93706a"),
    ("galerie-4.svg", 800, 800, "Momentka 4", "#d6cbbf", "#6e655d"),
    ("galerie-5.svg", 800, 1000, "Momentka 5", "#e1d4c4", "#857263"),
    ("galerie-6.svg", 800, 800, "Momentka 6", "#dccabd", "#7f6a60"),
    ("misto.svg", 1200, 800, "Místo konání", "#d4cdbf", "#6a6a5c"),
]


def photo(w, h, caption, c1, c2):
    extra = f"""
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
  <radialGradient id="v" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient>
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="{random.randint(1, 99)}"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .09 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
</defs>"""
    cx, cy = w / 2, h / 2
    r = min(w, h) * 0.11
    body = f"""
<rect width="{w}" height="{h}" fill="url(#g)"/>
<rect width="{w}" height="{h}" fill="url(#v)"/>
<rect width="{w}" height="{h}" filter="url(#grain)"/>
<g fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="{max(2, r*0.05):.1f}">
  <circle cx="{cx - r*0.45:.0f}" cy="{cy - r*0.3:.0f}" r="{r:.0f}"/>
  <circle cx="{cx + r*0.45:.0f}" cy="{cy - r*0.3:.0f}" r="{r:.0f}"/>
</g>
<g font-family="Didot, Georgia, serif" fill="#fff" text-anchor="middle">
  <text x="{cx}" y="{cy + r*1.25:.0f}" font-size="{r*0.32:.0f}" font-style="italic" fill-opacity=".92">{caption}</text>
  <text x="{cx}" y="{cy + r*1.65:.0f}" font-size="{r*0.17:.0f}" letter-spacing="{r*0.05:.0f}" fill-opacity=".7">DUMMY FOTO · {w}×{h}</text>
</g>"""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice">{extra}{body}</svg>\n'


def favicon():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<circle cx="32" cy="32" r="30" fill="{RED}"/>
<circle cx="32" cy="32" r="25" fill="none" stroke="#F6F1E9" stroke-opacity=".5" stroke-width="1"/>
<text x="32" y="41" text-anchor="middle" font-family="Didot, Georgia, serif" font-size="24" fill="#F6F1E9">M&amp;J</text>
</svg>
"""


def main():
    (IMG / "foto").mkdir(parents=True, exist_ok=True)
    (IMG / "florals-corner.svg").write_text(bouquet_corner())
    (IMG / "divider.svg").write_text(divider())
    (IMG / "sprig.svg").write_text(sprig())
    (IMG / "pozvanka.svg").write_text(invite())
    (IMG / "favicon.svg").write_text(favicon())
    for name, w, h, cap, c1, c2 in PHOTOS:
        (IMG / "foto" / name).write_text(photo(w, h, cap, c1, c2))
    print("Artwork written to", IMG)


if __name__ == "__main__":
    main()
