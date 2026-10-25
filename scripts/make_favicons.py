#!/usr/bin/env python3
"""The favicon set: an S in Schibsted Grotesk, paper on ink, with the accent rule.

Run once when the mark changes: python3 scripts/make_favicons.py
"""

import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw

from og_cards import ACCENT, BG, INK, FONT, font

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "favicons"


def mark(px):
    """Square ink tile, a paper S, the accent rule under it. Drawn at 4x, scaled down."""
    n = px * 4
    im = Image.new("RGB", (n, n), INK)
    d = ImageDraw.Draw(im)
    f = font(int(n * 0.74), 700)
    d.text((n / 2, n * 0.47), "S", font=f, fill=BG, anchor="mm")
    h = max(4, round(n * 0.07))
    d.rectangle([round(n * 0.3), round(n * 0.82), round(n * 0.7), round(n * 0.82) + h], fill=ACCENT)
    return im.resize((px, px), Image.LANCZOS)


def pinned_svg():
    """Monochrome mask icon: the tile with the S knocked out of it."""
    tt = instancer.instantiateVariableFont(TTFont(str(FONT)), {"wght": 700})
    gs = tt.getGlyphSet()
    g = gs[tt.getBestCmap()[ord("S")]]
    upm = tt["head"].unitsPerEm
    size = 500
    scale = size * 0.74 / upm
    # Centre the glyph's bounding box in the tile.
    from fontTools.pens.boundsPen import BoundsPen
    bp = BoundsPen(gs)
    g.draw(bp)
    x0, y0, x1, y1 = bp.bounds
    dx = size / 2 - (x0 + x1) / 2 * scale
    dy = size * 0.47 + (y0 + y1) / 2 * scale
    pen = SVGPathPen(gs)
    g.draw(TransformPen(pen, (scale, 0, 0, -scale, dx, dy)))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
        f'<path fill-rule="evenodd" d="M0 0H{size}V{size}H0Z {pen.getCommands()} '
        f'M150 410H350V445H150Z"/></svg>\n'
    )


def main():
    for name, px in [("favicon-16x16.png", 16), ("favicon-32x32.png", 32),
                     ("apple-touch-icon.png", 180), ("android-chrome-192x192.png", 192),
                     ("android-chrome-384x384.png", 384), ("mstile-150x150.png", 150)]:
        mark(px).save(OUT / name, optimize=True)
    mark(48).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    (OUT / "safari-pinned-tab.svg").write_text(pinned_svg(), encoding="utf-8")


if __name__ == "__main__":
    main()
