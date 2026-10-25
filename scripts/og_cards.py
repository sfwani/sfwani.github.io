"""Link preview images (1200x630) for the homepage and every advisory page.

Drawn from the same rows as the pages, so a shared link can never show a count
or a score the site no longer carries, the way the old hand-made ogp.png did.
Set in the site's own face and palette: paper, ink, hairlines, one accent.
Schibsted Grotesk ships beside this file under the SIL Open Font License.
"""

import pathlib

from PIL import Image, ImageDraw, ImageFont

W, H, M = 1200, 630, 80
FONT = pathlib.Path(__file__).resolve().parent / "fonts" / "SchibstedGrotesk.ttf"

BG = "#f2f1ec"
INK = "#141410"
INK_2 = "#56554e"
RULE = "#c6c4ba"
ACCENT = "#c02d14"
SEV = {"critical": "#8f1d07", "high": "#ad4313", "medium": "#80600c", "low": "#5f6b53"}


def font(size, weight=400):
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_axes([weight])
    return f


def tracked(d, xy, text, f, fill, track=0.12, anchor="ls"):
    """Uppercase label with letter spacing, which Pillow has no setting for."""
    x, y = xy
    gap = f.size * track
    if anchor == "rs":
        x -= sum(d.textlength(c, font=f) + gap for c in text) - gap
    for c in text:
        d.text((x, y), c, font=f, fill=fill, anchor="ls")
        x += d.textlength(c, font=f) + gap


def wrap(d, text, f, width, lines):
    """Greedy word wrap to at most `lines` lines, the last one ellipsised."""
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
            continue
        out.append(cur)
        cur = w
        if len(out) == lines:
            break
    if len(out) < lines and cur:
        out.append(cur)
    elif cur and len(out) == lines:
        last = out[-1]
        while last and d.textlength(last + "…", font=f) > width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        out[-1] = last.rstrip(" ,.:;") + "…"
    return out


def canvas():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([M, 64, M + 56, 69], fill=ACCENT)
    return im, d


def advisory_card(path, name, project, summary, score, severity, scheme, cwe):
    im, d = canvas()
    lab = font(19, 700)
    tracked(d, (M, 110), "SECURITY ADVISORY", lab, INK_2)
    tracked(d, (W - M, 110), "SFWANI.GITHUB.IO", lab, INK_2, anchor="rs")
    d.text((M, 196), name, font=font(64, 600), fill=INK, anchor="ls")
    tf = font(38, 500)
    y = 262
    for line in wrap(d, summary, tf, W - 2 * M, 3):
        d.text((M, y), line, font=tf, fill=INK, anchor="lt")
        y += 50
    d.line([(M, 470), (W - M, 470)], fill=INK, width=2)
    col = SEV.get((severity or "").lower(), INK_2)
    if score is not None:
        num = f"{score:.1f}"
        nf = font(96, 500)
        d.text((M - 4, 590), num, font=nf, fill=col, anchor="ls")
        x = M + d.textlength(num, font=nf) + 22
        tracked(d, (x, 548), (severity or "").upper(), font(22, 700), col)
        d.text((x, 586), scheme, font=font(22, 400), fill=INK_2, anchor="ls")
    else:
        tracked(d, (M, 560), (severity or "").upper(), font(30, 700), col)
    d.text((W - M, 548), project, font=font(30, 600), fill=INK, anchor="rs")
    d.text((W - M, 586), cwe or "", font=font(22, 400), fill=INK_2, anchor="rs")
    im.save(path, optimize=True)


def home_card(path, figures):
    im, d = canvas()
    lab = font(19, 700)
    tracked(d, (M, 110), "SECURITY RESEARCH", lab, INK_2)
    tracked(d, (W - M, 110), "SFWANI.GITHUB.IO", lab, INK_2, anchor="rs")
    d.text((M, 250), "Sanaan Fayaz Wani", font=font(92, 600), fill=INK, anchor="ls")
    sub = font(34, 400)
    for i, line in enumerate(wrap(d, "Vulnerabilities in AI agent frameworks and the infrastructure that runs large language models.", sub, W - 2 * M, 2)):
        d.text((M, 300 + i * 46), line, font=sub, fill=INK_2, anchor="lt")
    d.line([(M, 470), (W - M, 470)], fill=INK, width=2)
    x = M
    for v, k in figures:
        nf = font(64, 500)
        d.text((x, 572), str(v), font=nf, fill=INK, anchor="ls")
        d.text((x, 604), k, font=font(22, 400), fill=INK_2, anchor="ls")
        x += 360
    im.save(path, optimize=True)
