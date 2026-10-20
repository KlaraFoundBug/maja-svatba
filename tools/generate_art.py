#!/usr/bin/env python3
"""Generates the dummy invite card.

Run from the repo root:  python3 tools/generate_art.py
Replace img/pozvanka.svg with a photo/scan of the real invite whenever you have it.
"""
from pathlib import Path

IMG = Path(__file__).resolve().parent.parent / "img"
RED = "#B3211E"
INK = "#2A211E"


def invite():
    W, H = 600, 840
    # same typeface as the site (the page inlines this SVG, so the web font applies)
    serif = "'Cormorant Garamond', 'Hoefler Text', Garamond, Georgia, serif"
    script = serif
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/>
    <feColorMatrix values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .45  0 0 0 .07 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="#FBF7F0"/>
<rect width="{W}" height="{H}" filter="url(#paper)"/>
<rect x="24" y="24" width="{W-48}" height="{H-48}" fill="none" stroke="{RED}" stroke-width="1.2"/>
<rect x="32" y="32" width="{W-64}" height="{H-64}" fill="none" stroke="{RED}" stroke-width=".5"/>
<g font-family="{serif}" fill="{INK}" text-anchor="middle">
  <circle cx="300" cy="135" r="46" fill="none" stroke="{RED}" stroke-width=".8"/>
  <text x="300" y="148" font-size="34" letter-spacing="2">M<tspan font-style="italic" fill="{RED}" font-size="32">&amp;</tspan>M</text>
  <text x="300" y="242" font-size="14" letter-spacing="5">SPOLU S RODIČI</text>
  <text x="300" y="266" font-size="14" letter-spacing="5">VÁS SRDEČNĚ ZVOU</text>
  <text x="300" y="358" font-size="66" letter-spacing="6">MÁJA</text>
  <text x="300" y="420" font-size="58" font-style="italic" fill="{RED}">&amp;</text>
  <text x="300" y="490" font-size="66" letter-spacing="6">MÍŠA</text>
  <text x="300" y="548" font-size="14" letter-spacing="5">NA SVŮJ SVATEBNÍ DEN</text>
  <line x1="190" y1="580" x2="410" y2="580" stroke="{RED}" stroke-width=".8"/>
  <text x="300" y="616" font-size="26" letter-spacing="8">5 · 6 · 2027</text>
  <line x1="190" y1="636" x2="410" y2="636" stroke="{RED}" stroke-width=".8"/>
  <text x="300" y="676" font-size="14" letter-spacing="4">OBŘAD VE 13:00</text>
  <text x="300" y="704" font-size="18" font-style="italic">Stodola Plástovice</text>
  <text x="300" y="772" font-size="24" font-style="italic" fill="{RED}">Těšíme se na vás</text>
</g>
</svg>
"""


if __name__ == "__main__":
    (IMG / "pozvanka.svg").write_text(invite())
    # img/favicon.svg is now a hand-drawn cat, so it is not regenerated here
    print("Artwork written to", IMG)
