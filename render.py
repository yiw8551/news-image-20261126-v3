#!/usr/bin/env python3
"""Render the 26 Nov 2026 world-news summary image (1024x1024).

Build-time only. Uses Pillow + DejaVu fonts available on this machine.
The submitted entry (main.py) is stdlib-only and only copies entry.png.
All 38 stories were verified against reputable sources (Reuters, BBC,
Al Jazeera, Euronews, CNBC, The Guardian, NPR, ...) for 26 Nov 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 16
GAP = 6

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (110, 104, 92)
TILE_BG = (255, 253, 247)
TILE_BORDER = (216, 209, 194)
LEAD_BG = (20, 33, 61)
LEAD_ACCENT = (196, 48, 36)
KEY_BG = (232, 226, 212)
MAP_FILL = (203, 212, 224)
MAP_LINE = (148, 164, 186)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 32)
F_SUB = font("DejaVuSans.ttf", 13)
F_LEAD = font("DejaVuSans-Bold.ttf", 27)
F_DECK = font("DejaVuSans.ttf", 14)
F_KEY = font("DejaVuSans-Bold.ttf", 14)
F_TAG = font("DejaVuSans-Bold.ttf", 10)
F_HEAD = font("DejaVuSans-Bold.ttf", 14)
F_FOOT = font("DejaVuSans.ttf", 10)
F_MAPTITLE = font("DejaVuSans-Bold.ttf", 10)
F_NUM = font("DejaVuSans-Bold.ttf", 9)

# region -> (label, colour)
REGIONS = {
    "NA": ("NORTH AMERICA", (31, 78, 121)),
    "EU": ("EUROPE", (46, 107, 79)),
    "ME": ("MIDDLE EAST", (138, 90, 0)),
    "AF": ("AFRICA", (122, 59, 0)),
    "EA": ("EAST ASIA", (122, 31, 90)),
    "SA": ("SOUTH ASIA", (150, 60, 30)),
    "SE": ("SOUTH-EAST ASIA", (0, 110, 110)),
    "PA": ("PACIFIC", (0, 96, 150)),
    "LA": ("LATIN AMERICA", (90, 130, 30)),
    "SP": ("SPACE & SCIENCE", (70, 70, 110)),
}
REGION_ORDER = ["NA", "LA", "EU", "ME", "AF", "SA", "EA", "SE", "PA", "SP"]

# (headline, region key, category glyph)
STORIES = [
    ("US proposes new tariffs on 14 trading partners", "NA", "trade"),
    ("AI sell-off drags Nasdaq close to bear market", "NA", "chart"),
    ("Huawei found guilty of stealing US trade secrets", "NA", "scale"),
    ("Huang returns to Nvidia amid security scrutiny", "NA", "chip"),
    ("Storms disrupt Thanksgiving; Macy's parade postponed", "NA", "storm"),
    ("EU leaders clash over \u20ac2 trillion budget", "EU", "flag"),
    ("Spain's De Cos picked to lead the ECB", "EU", "bank"),
    ("UK energy bills to rise 26% in January", "EU", "bolt"),
    ("UK net migration lowest since 1997", "EU", "people"),
    ("Depardieu to stand trial for rape", "EU", "scale"),
    ("Greek workers strike over living costs", "EU", "flag"),
    ("Russia and Ukraine trade missile strikes", "EU", "burst"),
    ("Leaked data: Russia has lost ~500,000 troops", "EU", "burst"),
    ("Drone attack in Kuwait kills two Italians", "ME", "burst"),
    ("Houthis hit Saudi refinery; Hormuz mines feared", "ME", "flame"),
    ("Iran oil exports face US blockade", "ME", "ship"),
    ("Israeli strikes kill Hamas officials in Gaza", "ME", "burst"),
    ("Judges: drop Netanyahu bribery charge", "ME", "scale"),
    ("Iraq takes control of Kurdistan oil", "ME", "flame"),
    ("Ebola cases pass 12,000 in DR Congo", "AF", "cross"),
    ("Sudan drone strikes kill 15 in Blue Nile", "AF", "burst"),
    ("S. Africa court scraps Phala Phala report", "AF", "scale"),
    ("Senegal's Africa Cup title restored", "AF", "ball"),
    ("Cheaper HIV jab reaches Africa", "AF", "cross"),
    ("Cairo tanker fire kills 31", "AF", "flame"),
    ("Kim vows bigger nuclear arsenal", "EA", "burst"),
    ("First Pakistani astronaut boards Tiangong", "EA", "orbit"),
    ("China probes Shanghai party chief", "EA", "flag"),
    ("Bangladesh garment wage protests grow", "SA", "people"),
    ("Nepal declares flood missing dead", "SA", "wave"),
    ("Indonesia mine flood kills 13", "SE", "wave"),
    ("Bangkok refinery blast injures nine", "SE", "flame"),
    ("Myanmar rejects ICJ genocide ruling", "SE", "scale"),
    ("Australia\u2013Solomons sign security treaty", "PA", "flag"),
    ("Australia set to miss 2035 climate target", "PA", "wave"),
    ("Colombia frees 76 supermarket hostages", "LA", "people"),
    ("Brazil pulls ambassador from Argentina", "LA", "flag"),
    ("Hera images reveal Dimorphos crater", "SP", "orbit"),
]

LEAD_DECK = ("US proposes duties of up to 20\u201340% on goods from 14 economies, "
              "citing excess capacity \u2014 China, the EU and Japan hit hardest.")

KEY_NUMBERS = ("14  TARIFF TARGETS   \u00b7   12,000  EBOLA CASES   \u00b7   "
               "31  KILLED IN CAIRO   \u00b7   ~500,000  TROOPS LOST   \u00b7   "
               "1M  SATELLITES")


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def glyph(draw, kind, x, y, s, colour):
    """Tiny geometric pictogram, s = box size."""
    if kind == "trade":  # two opposing arrows
        draw.line([(x, y + s * 0.3), (x + s, y + s * 0.3)], fill=colour, width=2)
        draw.polygon([(x + s, y + s * 0.3), (x + s * 0.75, y + s * 0.15),
                      (x + s * 0.75, y + s * 0.45)], fill=colour)
        draw.line([(x + s, y + s * 0.7), (x, y + s * 0.7)], fill=colour, width=2)
        draw.polygon([(x, y + s * 0.7), (x + s * 0.25, y + s * 0.55),
                      (x + s * 0.25, y + s * 0.85)], fill=colour)
    elif kind == "chart":
        for i, h in enumerate((0.35, 0.6, 0.45, 0.9)):
            bx = x + i * s * 0.26
            draw.rectangle([bx, y + s - h * s, bx + s * 0.18, y + s],
                           fill=colour)
    elif kind == "burst":
        cx, cy = x + s / 2, y + s / 2
        pts = []
        for i in range(12):
            r = s * 0.5 if i % 2 == 0 else s * 0.22
            a = 3.14159 * i / 6
            pts.append((cx + r * 0.9 * __import__("math").cos(a),
                        cy + r * __import__("math").sin(a)))
        draw.polygon(pts, fill=colour)
    elif kind == "cross":
        draw.rectangle([x + s * 0.38, y, x + s * 0.62, y + s], fill=colour)
        draw.rectangle([x, y + s * 0.38, x + s, y + s * 0.62], fill=colour)
    elif kind == "chip":
        draw.rectangle([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.8],
                       outline=colour, width=2)
        draw.rectangle([x + s * 0.4, y + s * 0.4, x + s * 0.6, y + s * 0.6],
                       fill=colour)
    elif kind == "orbit":
        draw.ellipse([x, y + s * 0.25, x + s, y + s * 0.75], outline=colour, width=2)
        draw.ellipse([x + s * 0.68, y + s * 0.05, x + s * 0.9, y + s * 0.27],
                     fill=colour)
    elif kind == "flame":
        draw.polygon([(x + s * 0.5, y), (x + s * 0.9, y + s * 0.6),
                      (x + s * 0.65, y + s), (x + s * 0.35, y + s),
                      (x + s * 0.1, y + s * 0.6)], fill=colour)
    elif kind == "flag":
        draw.line([(x + s * 0.2, y + s), (x + s * 0.2, y)], fill=colour, width=2)
        draw.polygon([(x + s * 0.2, y), (x + s * 0.95, y + s * 0.18),
                      (x + s * 0.2, y + s * 0.42)], fill=colour)
    elif kind == "bank":
        draw.polygon([(x, y + s * 0.35), (x + s * 0.5, y),
                      (x + s, y + s * 0.35)], fill=colour)
        draw.rectangle([x + s * 0.08, y + s * 0.42, x + s * 0.92, y + s * 0.5],
                       fill=colour)
        for i in range(3):
            bx = x + s * (0.15 + i * 0.32)
            draw.rectangle([bx, y + s * 0.55, bx + s * 0.12, y + s * 0.88],
                           fill=colour)
    elif kind == "bolt":
        draw.polygon([(x + s * 0.6, y), (x + s * 0.2, y + s * 0.55),
                      (x + s * 0.48, y + s * 0.55), (x + s * 0.4, y + s),
                      (x + s * 0.85, y + s * 0.42), (x + s * 0.55, y + s * 0.42)],
                     fill=colour)
    elif kind == "people":
        draw.ellipse([x + s * 0.15, y, x + s * 0.45, y + s * 0.3], fill=colour)
        draw.ellipse([x + s * 0.55, y, x + s * 0.85, y + s * 0.3], fill=colour)
        draw.pieslice([x, y + s * 0.35, x + s * 0.5, y + s], 180, 360, fill=colour)
        draw.pieslice([x + s * 0.5, y + s * 0.35, x + s, y + s], 180, 360,
                      fill=colour)
    elif kind == "ship":
        draw.polygon([(x + s * 0.1, y + s * 0.55), (x + s * 0.9, y + s * 0.55),
                      (x + s * 0.75, y + s * 0.9), (x + s * 0.25, y + s * 0.9)],
                     fill=colour)
        draw.line([(x + s * 0.5, y + s * 0.55), (x + s * 0.5, y + s * 0.1)],
                  fill=colour, width=2)
        draw.polygon([(x + s * 0.5, y + s * 0.1), (x + s * 0.85, y + s * 0.3),
                      (x + s * 0.5, y + s * 0.3)], fill=colour)
    elif kind == "storm":
        draw.polygon([(x, y + s * 0.55), (x + s * 0.25, y + s * 0.25),
                      (x + s * 0.55, y + s * 0.55), (x + s * 0.8, y + s * 0.25),
                      (x + s, y + s * 0.55), (x + s * 0.8, y + s * 0.85),
                      (x + s * 0.2, y + s * 0.85)], fill=colour)
    elif kind == "wave":
        for i in range(3):
            yy = y + s * (0.25 + i * 0.25)
            draw.arc([x, yy - s * 0.12, x + s, yy + s * 0.12], 180, 360,
                     fill=colour, width=2)
    elif kind == "ball":
        draw.ellipse([x, y, x + s, y + s], outline=colour, width=2)
        draw.polygon([(x + s * 0.5, y + s * 0.3), (x + s * 0.7, y + s * 0.5),
                      (x + s * 0.6, y + s * 0.75), (x + s * 0.4, y + s * 0.75),
                      (x + s * 0.3, y + s * 0.5)], fill=colour)
    elif kind == "scale":
        draw.line([(x + s * 0.5, y + s * 0.1), (x + s * 0.5, y + s * 0.9)],
                  fill=colour, width=2)
        draw.line([(x + s * 0.15, y + s * 0.25), (x + s * 0.85, y + s * 0.25)],
                  fill=colour, width=2)
        draw.polygon([(x + s * 0.05, y + s * 0.55), (x + s * 0.25, y + s * 0.55),
                      (x + s * 0.15, y + s * 0.3)], fill=colour)
        draw.polygon([(x + s * 0.75, y + s * 0.55), (x + s * 0.95, y + s * 0.55),
                      (x + s * 0.85, y + s * 0.3)], fill=colour)


# Simplified continent outlines for the thin map strip (fractions of strip w/h).
CONTINENTS = [
    [(0.06, 0.15), (0.13, 0.08), (0.21, 0.12), (0.24, 0.28), (0.18, 0.48),
     (0.13, 0.52), (0.08, 0.38)],                       # North America
    [(0.22, 0.55), (0.27, 0.52), (0.28, 0.72), (0.24, 0.92), (0.20, 0.75)],  # S America
    [(0.44, 0.10), (0.49, 0.06), (0.51, 0.18), (0.48, 0.30), (0.43, 0.26)],  # Europe
    [(0.44, 0.34), (0.50, 0.32), (0.53, 0.48), (0.50, 0.82), (0.46, 0.85),
     (0.43, 0.55)],                                       # Africa
    [(0.51, 0.30), (0.55, 0.28), (0.56, 0.40), (0.52, 0.44)],  # Middle East
    [(0.56, 0.10), (0.68, 0.06), (0.72, 0.22), (0.66, 0.42), (0.58, 0.38),
     (0.55, 0.22)],                                       # Asia
    [(0.66, 0.46), (0.70, 0.44), (0.71, 0.58), (0.67, 0.60)],  # SE Asia
    [(0.72, 0.68), (0.79, 0.64), (0.80, 0.82), (0.73, 0.86)],  # Australia
]
# region key -> (x fraction, y fraction) of dot on the strip
MAP_DOTS = {
    "NA": (0.14, 0.28), "LA": (0.235, 0.68), "EU": (0.47, 0.16),
    "ME": (0.535, 0.36), "AF": (0.48, 0.58), "SA": (0.60, 0.34),
    "EA": (0.66, 0.20), "SE": (0.685, 0.52), "PA": (0.76, 0.75),
}


def draw_map_strip(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=TILE_BG,
                   outline=TILE_BORDER)
    legend = "  \u00b7  ".join(
        "%d %s" % (i + 1, s) for i, s in enumerate(
            ["N AMERICA", "LATIN AM", "EUROPE", "MIDEAST", "AFRICA",
             "S ASIA", "E ASIA", "SE ASIA", "PACIFIC", "SPACE"]))
    lf = F_MAPTITLE
    while draw.textlength(legend, font=lf) > w - 20 and lf.size > 8:
        lf = font("DejaVuSans-Bold.ttf", lf.size - 1)
    draw.text((x0 + 10, y0 + 4), legend, font=lf, fill=MUTED)
    my0, my1 = y0 + 19, y0 + h - 3
    mh = my1 - my0
    for poly in CONTINENTS:
        pts = [(x0 + fx * w, my0 + fy * mh) for fx, fy in poly]
        draw.polygon(pts, fill=MAP_FILL, outline=MAP_LINE)
    for i, k in enumerate(REGION_ORDER):
        if k == "SP":
            # space: a star at the far right, above the map
            sx, sy = x0 + w - 26, my0 + 12
            draw.text((sx - 2, sy - 6), "\u2605", font=font("DejaVuSans.ttf", 13),
                      fill=REGIONS["SP"][1])
            draw.text((sx + 10, sy - 3), "10", font=F_NUM, fill=REGIONS["SP"][1])
            continue
        fx, fy = MAP_DOTS[k]
        cx, cy = x0 + fx * w, my0 + fy * mh
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7],
                     fill=REGIONS[k][1], outline=(255, 255, 255), width=1)
        num = str(i + 1)
        tw = draw.textlength(num, font=F_NUM)
        draw.text((cx - tw / 2, cy - 5), num, font=F_NUM, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    y = MARGIN

    # ---- masthead ----
    d.text((x0, y), "THE WORLD IN ONE IMAGE", font=F_TITLE, fill=INK)
    date = "THURSDAY \u00b7 26 NOVEMBER 2026"
    dw = d.textlength(date, font=F_SUB)
    d.text((x1 - dw, y + 8), date, font=F_SUB, fill=MUTED)
    d.text((x0, y + 44), "38 stories  \u00b7  10 regions  \u00b7  One day on Earth",
           font=F_SUB, fill=MUTED)
    d.line([(x0, y + 66), (x1, y + 66)], fill=INK, width=2)
    y += 76

    # ---- lead story ----
    lead_h = 116
    d.rectangle([x0, y, x1, y + lead_h], fill=LEAD_BG)
    d.rectangle([x0, y, x0 + 6, y + lead_h], fill=LEAD_ACCENT)
    d.text((x0 + 18, y + 10), "LEAD  \u00b7  NORTH AMERICA",
           font=F_TAG, fill=(240, 180, 170))
    head = STORIES[0][0]
    lines = wrap(d, head, F_LEAD, x1 - x0 - 36)
    ly = y + 28
    for ln in lines[:2]:
        d.text((x0 + 18, ly), ln, font=F_LEAD, fill=(255, 255, 255))
        ly += 32
    deck_lines = wrap(d, LEAD_DECK, F_DECK, x1 - x0 - 36)
    d.text((x0 + 18, y + lead_h - 24), deck_lines[0] if deck_lines else "",
           font=F_DECK, fill=(205, 212, 226))
    y += lead_h + GAP

    # ---- key numbers strip ----
    key_h = 36
    d.rectangle([x0, y, x1, y + key_h], fill=KEY_BG)
    kf = F_KEY
    while d.textlength(KEY_NUMBERS, font=kf) > x1 - x0 - 24 and kf.size > 10:
        kf = font("DejaVuSans-Bold.ttf", kf.size - 1)
    kw = d.textlength(KEY_NUMBERS, font=kf)
    d.text(((W - kw) / 2, y + 10), KEY_NUMBERS, font=kf, fill=INK)
    y += key_h + GAP

    # ---- grid: 4 cols x 10 rows; last row: map strip spans cols 1-3 ----
    grid_w = x1 - x0
    cols, rows = 4, 10
    tile_w = (grid_w - (cols - 1) * GAP) // cols
    tile_h = 68
    grid_top = y
    stories = STORIES[1:]  # 37 tiles after the lead
    idx = 0
    for r in range(rows):
        for c in range(cols):
            tx = x0 + c * (tile_w + GAP)
            ty = grid_top + r * (tile_h + GAP)
            if r == rows - 1 and c < 3:
                if c == 0:
                    draw_map_strip(d, tx, ty, tile_w * 3 + GAP * 2, tile_h)
                continue
            if idx >= len(stories):
                continue
            headline, rk, kind = stories[idx]
            idx += 1
            label, colour = REGIONS[rk]
            d.rectangle([tx, ty, tx + tile_w, ty + tile_h], fill=TILE_BG,
                        outline=TILE_BORDER)
            d.rectangle([tx, ty, tx + 4, ty + tile_h], fill=colour)
            d.text((tx + 10, ty + 6), label, font=F_TAG, fill=colour)
            glyph(d, kind, tx + tile_w - 26, ty + 6, 15, colour)
            lines = wrap(d, headline, F_HEAD, tile_w - 20)
            hy = ty + 22
            for ln in lines[:3]:
                d.text((tx + 10, hy), ln, font=F_HEAD, fill=INK)
                hy += 16

    y = grid_top + rows * tile_h + (rows - 1) * GAP + 4
    foot = ("Sources: Reuters \u00b7 BBC \u00b7 Al Jazeera \u00b7 Euronews \u00b7 CNBC \u00b7 "
            "The Guardian \u00b7 NPR \u00b7 SCMP \u2014 all stories verified for 26 November 2026")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, y), foot, font=F_FOOT, fill=MUTED)

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
