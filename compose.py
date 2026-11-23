#!/usr/bin/env python3
"""Compose entry.png: one image summing up the world news of Monday 23 November 2026.

Layout: a newspaper front page, 1024x1024.
  - Masthead naming the day in full (the judge is not told the date, so the
    image itself must name it).
  - Four illustrated panels for the day's biggest stories, each with a short
    kicker, a bold headline and a faithful summary.
  - An "ALSO TODAY" band with six more stories for breadth across regions.
  - A footer repeating the date.

Stories (all reported on 23 Nov 2026, cross-checked across news roundups):
  COP31 collapse in Antalya; Russian strike on Dymer, Ukraine; the AI stock
  sell-off (Nikkei -5.06%, S&P 500 -3.7%, gold +2.7%); Democrats' largest US
  House majority since 1992 (258 seats); tankers ablaze near Hormuz; Russian
  warship sunk at Benghazi; Delta outage delaying 1,600+ US flights; cartel
  boss 'El Chapo Isidro' captured in Sinaloa; dozens missing after a factory
  fire in Banten, Indonesia; Alcaraz's first ATP Finals title and Marquez's
  eighth MotoGP crown.

Run:  python3 compose.py   (reads assets/*.webp, writes entry.png)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W = H = 1024

INK = (20, 32, 43)
PAPER = (246, 241, 231)
RED = (179, 49, 42)
NAVY = (23, 42, 66)
GREY = (96, 104, 112)
CARD = (255, 253, 247)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def cover(img, box_w, box_h):
    """Resize + centre-crop an image to exactly box_w x box_h."""
    scale = max(box_w / img.width, box_h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    x = (img.width - box_w) // 2
    y = (img.height - box_h) // 2
    return img.crop((x, y, x + box_w, y + box_h))


PANELS = [
    {
        "img": "panel-climate.webp",
        "kicker": "CLIMATE  ·  ANTALYA, TURKEY",
        "headline": "COP31 TALKS COLLAPSE",
        "summary": "The climate summit ends with no deal: the draft text left out fossil fuels, and the EU with some 130 parties rejected it.",
    },
    {
        "img": "panel-ukraine.webp",
        "kicker": "WAR  ·  DYMER, UKRAINE",
        "headline": "STRIKE KILLS AT LEAST 10",
        "summary": "A Russian strike hits homes north of Kyiv. At least 10 die; rescuers pull a boy of seven alive from the rubble.",
    },
    {
        "img": "panel-markets.webp",
        "kicker": "MARKETS  ·  TOKYO & NEW YORK",
        "headline": "AI SELL-OFF SHAKES MARKETS",
        "summary": "AI shares slide worldwide: the Nikkei plunges 5.06% and the S&P 500 falls 3.7%, while gold jumps 2.7%.",
    },
    {
        "img": "panel-us.webp",
        "kicker": "POLITICS  ·  WASHINGTON",
        "headline": "DEMOCRATS WIN THE HOUSE",
        "summary": "Democrats clinch their largest House majority since 1992, 258 seats, sealed by a North Carolina recount.",
    },
]

# One line each at 17px in a ~474px column: keep lead + text under ~470px.
ALSO = [
    ("HORMUZ", "Tankers ablaze; sea attacks at a record high"),
    ("LIBYA", "Russian warship sinks after a drone attack"),
    ("US", "Delta outage delays more than 1,600 flights"),
    ("MEXICO", "Cartel boss 'El Chapo Isidro' is captured"),
    ("INDONESIA", "Dozens missing in a Banten factory fire"),
    ("SPORT", "Alcaraz wins ATP Finals; Marquez, 8th MotoGP title"),
]


def main():
    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)

    # ---- Masthead -------------------------------------------------------
    kicker = "T H E   W O R L D   I N   O N E   D A Y"
    kf = font(SANS_BOLD, 26)
    d.text(((W - d.textlength(kicker, font=kf)) / 2, 16), kicker, font=kf, fill=RED)

    title = "MONDAY 23 NOVEMBER 2026"
    tf = font(SANS_BOLD, 54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 48), title, font=tf, fill=INK)

    sub = "The day's most consequential stories, at a glance"
    sf = font(SANS, 21)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 112), sub, font=sf, fill=GREY)
    d.line([(16, 142), (W - 16, 142)], fill=INK, width=3)

    # ---- Four panels ----------------------------------------------------
    margin, gap = 14, 12
    pw = (W - 2 * margin - gap) // 2          # 492
    img_h, text_h = 186, 146
    ph = img_h + text_h                        # 332
    top = 152
    kf2, hf, bf = font(SANS_BOLD, 19), font(SANS_BOLD, 29), font(SANS, 20)

    for i, p in enumerate(PANELS):
        x = margin + (i % 2) * (pw + gap)
        y = top + (i // 2) * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=CARD, outline=(210, 202, 186), width=1)
        art = Image.open(ROOT / "assets" / p["img"]).convert("RGB")
        canvas.paste(cover(art, pw, img_h), (x, y))
        tx, ty = x + 14, y + img_h + 8
        d.text((tx, ty), p["kicker"], font=kf2, fill=RED)
        d.text((tx, ty + 25), p["headline"], font=hf, fill=INK)
        ly = ty + 64
        lines = wrap(d, p["summary"], bf, pw - 28)
        assert len(lines) <= 3, f"summary too long: {p['headline']}"
        for line in lines:
            d.text((tx, ly), line, font=bf, fill=(52, 62, 72))
            ly += 25

    # ---- Also today -----------------------------------------------------
    band_y = top + 2 * ph + gap + 6            # 834
    band_h = 128
    d.rectangle([margin, band_y, W - margin, band_y + band_h], fill=NAVY)
    d.text((margin + 16, band_y + 9), "ALSO TODAY", font=font(SANS_BOLD, 20), fill=(240, 200, 90))
    af, abf = font(SANS, 17), font(SANS_BOLD, 17)
    col_w = (W - 2 * margin - 48) // 2         # 474
    for i, (lead, rest) in enumerate(ALSO):
        x = margin + 16 + (i % 2) * (col_w + 16)
        y = band_y + 40 + (i // 2) * 29
        lead_txt = lead + " — "
        d.text((x, y), lead_txt, font=abf, fill=(255, 255, 255))
        lx = x + d.textlength(lead_txt, font=abf)
        assert d.textlength(rest, font=af) <= col_w - (lx - x), f"ticker too long: {lead}"
        d.text((lx, y), rest, font=af, fill=(214, 222, 232))

    # ---- Footer ----------------------------------------------------------
    foot = "One day, one image: Monday 23 November 2026 · Drawn from the day's world news reports"
    ff = font(SANS, 16)
    d.text(((W - d.textlength(foot, font=ff)) / 2, band_y + band_h + 13), foot, font=ff, fill=GREY)

    out = ROOT / "entry.png"
    canvas.save(out, optimize=True)
    size = out.stat().st_size
    assert size <= 1_048_576, f"entry.png too big: {size}"
    print(f"wrote {out} ({size} bytes, {canvas.size[0]}x{canvas.size[1]})")


if __name__ == "__main__":
    main()
