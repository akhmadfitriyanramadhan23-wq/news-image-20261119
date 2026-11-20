#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news image (1024x1024 PNG).

Front-page style, flat vector-style art drawn with Pillow primitives and
Liberation Sans (a freely licensed font installed on this machine). No
photo, no AI image model, no network: every pixel is drawn by this script
from the story list below, so the text is crisp and exactly as written.

Stories were checked against multiple same-day digests on 21 Nov 2026 WIB:
- ICJ genocide ruling: Medium/All Voices News brief, horizonapp.link,
  foreignexchanges.news, oneturn.news (all agree: ICJ ruled Thursday that
  Myanmar committed genocide against the Rohingya; Gambia v. Myanmar).
- Shenzhen trilateral summit + four-point "Declaration toward Peace":
  horizonapp.link, foreignexchanges.news, standardtopic.com.
- COP31 Antalya ministerial push: horizonapp.link.
- Gaza peace plan scored 4/26 by aid groups; IDF in Nuseirat:
  Medium brief, foreignexchanges.news, oneturn.news.
- Bangladesh violence, 28 districts, Yunus home torched: horizonapp.link.
- Hormuz / IEA energy warning, tanker attacks, 2 seafarers missing:
  horizonapp.link, standardtopic.com.
- EU EUR45bn Ukraine loan; Crimea bridge struck a third time that week:
  horizonapp.link, 10things.news, dailydigest.com.
- Also strip: Van Gogh record $190.4m (horizonapp.link); Voyager 1
  one-light-day milestone (rationaltimes.com); migrant boat off Senegal,
  dozens missing (standardtopic.com); Mongolia president resigns
  (foreignexchanges.news).

Run: python3 tools/make-image.py  ->  writes entry.png (<=1 MiB, 1024x1024).
"""
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "entry.png"

W = H = 1024
PAPER = (247, 242, 231)      # cream newsprint
INK = (18, 28, 46)           # near-black navy
NAVY = (23, 42, 74)
RED = (178, 34, 34)
GOLD = (198, 142, 38)
TEAL = (15, 118, 110)
GREEN = (34, 120, 62)
ORANGE = (204, 94, 24)
SLATE = (84, 96, 112)
CARD = (255, 255, 255)
RULE = (18, 28, 46)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, box, accent):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD, outline=RULE, width=2)
    draw.rectangle([x0, y0, x1, y0 + 10], fill=accent)


def scales_icon(draw, cx, cy, s, color):
    """Scales of justice, centred at (cx, cy), size s."""
    d = draw
    d.line([(cx, cy - s * 0.55), (cx, cy + s * 0.55)], fill=color, width=max(4, s // 18))
    d.line([(cx - s * 0.5, cy - s * 0.42), (cx + s * 0.5, cy - s * 0.42)], fill=color, width=max(4, s // 18))
    d.ellipse([cx - s * 0.07, cy - s * 0.62, cx + s * 0.07, cy - s * 0.48], fill=color)
    for sx in (-1, 1):
        px = cx + sx * s * 0.5
        d.line([(px, cy - s * 0.42), (px, cy - s * 0.05)], fill=color, width=max(3, s // 24))
        d.pieslice([px - s * 0.22, cy - s * 0.05, px + s * 0.22, cy + s * 0.28],
                   0, 180, fill=color)
    d.line([(cx - s * 0.3, cy + s * 0.55), (cx + s * 0.3, cy + s * 0.55)], fill=color, width=max(4, s // 18))


def skyline_icon(draw, box, color):
    x0, y0, x1, y1 = box
    heights = [0.55, 0.8, 0.45, 0.95, 0.65, 0.85, 0.5]
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        draw.rectangle([x0 + i * bw + 3, y1 - (y1 - y0) * h, x0 + (i + 1) * bw - 3, y1],
                       fill=color)


def leaf_icon(draw, cx, cy, s, color):
    # A simple leaf: two arcs meeting at the tips, with a centre vein.
    draw.pieslice([cx - s * 0.4, cy - s * 0.42, cx + s * 0.4, cy + s * 0.42], 200, 340,
                  fill=color)
    draw.pieslice([cx - s * 0.4, cy - s * 0.42, cx + s * 0.4, cy + s * 0.42], 20, 160,
                  fill=color)
    draw.line([(cx - s * 0.3, cy + s * 0.3), (cx + s * 0.3, cy - s * 0.3)],
              fill=PAPER, width=max(3, s // 20))


def aid_icon(draw, cx, cy, s, color):
    draw.ellipse([cx - s * 0.45, cy - s * 0.45, cx + s * 0.45, cy + s * 0.45],
                 outline=color, width=max(4, s // 16))
    w = s * 0.16
    draw.rectangle([cx - w, cy - s * 0.3, cx + w, cy + s * 0.3], fill=color)
    draw.rectangle([cx - s * 0.3, cy - w, cx + s * 0.3, cy + w], fill=color)


def flame_icon(draw, cx, cy, s, color):
    pts = [(cx, cy - s * 0.5), (cx + s * 0.28, cy - s * 0.05), (cx + s * 0.16, cy + s * 0.1),
           (cx + s * 0.34, cy + s * 0.32), (cx - s * 0.34, cy + s * 0.32),
           (cx - s * 0.16, cy + s * 0.1), (cx - s * 0.28, cy - s * 0.05)]
    draw.polygon(pts, fill=color)


def drop_icon(draw, cx, cy, s, color):
    draw.ellipse([cx - s * 0.3, cy - s * 0.18, cx + s * 0.3, cy + s * 0.42], fill=color)
    draw.polygon([(cx, cy - s * 0.5), (cx - s * 0.3, cy - s * 0.05), (cx + s * 0.3, cy - s * 0.05)],
                 fill=color)
    for i, yy in enumerate((cy + s * 0.52, cy + s * 0.62)):
        draw.arc([cx - s * 0.42, yy, cx + s * 0.42, yy + s * 0.16], 0, 180,
                 fill=color, width=max(3, s // 22))


def bridge_icon(draw, box, color):
    x0, y0, x1, y1 = box
    draw.arc([x0 + 8, y0 + 10, x1 - 8, y1 + 40], 180, 360, fill=color, width=6)
    draw.line([(x0 + 8, y1 - 8), (x1 - 8, y1 - 8)], fill=color, width=6)
    for fx in (0.25, 0.5, 0.75):
        x = x0 + (x1 - x0) * fx
        draw.line([(x, y0 + 26), (x, y1 - 8)], fill=color, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- Masthead ----
    d.text((W // 2, 18), "THE WORLD IN ONE DAY", font=font(FB, 58),
           fill=INK, anchor="ma")
    d.text((W // 2, 84), "T H U R S D A Y  ·  1 9  N O V E M B E R  2 0 2 6",
           font=font(FB, 26), fill=RED, anchor="ma")
    d.line([(M, 126), (W - M, 126)], fill=RULE, width=3)

    # ---- Lead story: ICJ ruling ----
    lx0, ly0, lx1, ly1 = M, 142, W - M, 452
    panel(d, (lx0, ly0, lx1, ly1), RED)
    # icon block on the left
    d.rectangle([lx0 + 2, ly0 + 12, lx0 + 268, ly1 - 2], fill=NAVY)
    scales_icon(d, lx0 + 135, ly0 + 165, 170, GOLD)
    d.text((lx0 + 135, ly1 - 62), "THE HAGUE", font=font(FB, 24), fill=(255, 255, 255),
           anchor="ma")
    tx = lx0 + 296
    tw = lx1 - tx - 24
    y = ly0 + 34
    d.text((tx, y), "WORLD COURT", font=font(FB, 24), fill=RED)
    y += 34
    y = text_block(d, (tx, y), "MYANMAR COMMITTED GENOCIDE, JUDGES RULE",
                   font(FB, 46), INK, tw, leading=54)
    y += 8
    text_block(d, (tx, y),
               "The International Court of Justice finds Myanmar's military "
               "acted with genocidal intent against the Rohingya in 2017 — "
               "the court's first such ruling against a state.",
               font(FR, 25), (40, 48, 66), tw, leading=33)

    # ---- Middle row: three panels ----
    # Each panel's text is fitted: the body font shrinks until headline +
    # body fit inside the panel, so nothing can overflow into the next row.
    y0, y1 = 468, 716
    cw = (W - 2 * M - 2 * 16) // 3

    def story_panel(x0, y0, x1, y1, kick, head, body, icon, accent, icon_top, icon_h):
        panel(d, (x0, y0, x1, y1), accent)
        if icon is skyline_icon or icon is bridge_icon:
            icon(d, (x0 + cw // 2 - 52, y0 + icon_top, x0 + cw // 2 + 52,
                     y0 + icon_top + icon_h), accent)
        else:
            icon(d, x0 + cw // 2, y0 + icon_top + icon_h // 2, icon_h, accent)
        yy = y0 + icon_top + icon_h + 12
        d.text((x0 + 16, yy), kick, font=font(FB, 17), fill=accent)
        yy += 26
        head_lines = wrap(d, head, font(FB, 26), cw - 32)
        body_size = 19
        while True:
            body_lines = wrap(d, body, font(FR, body_size), cw - 32)
            need = len(head_lines) * 30 + 6 + len(body_lines) * int(body_size * 1.3)
            if yy + need <= y1 - 12 or body_size <= 15:
                break
            body_size -= 1
        for line in head_lines:
            d.text((x0 + 16, yy), line, font=font(FB, 26), fill=INK)
            yy += 30
        yy += 6
        for line in body_lines:
            d.text((x0 + 16, yy), line, font=font(FR, body_size), fill=(40, 48, 66))
            yy += int(body_size * 1.3)

    stories = [
        ("SHENZHEN · SUMMIT", "THREE LEADERS, ONE DECLARATION",
         "Trump, Xi and Putin meet as a trio and sign a four-point "
         "'Declaration toward Peace' — silent on Ukraine and Iran.",
         skyline_icon, RED, 22, 62),
        ("ANTALYA · CLIMATE", "COP31 TALKS STALL",
         "Ministers meet late into the night in Turkey, trying to unblock "
         "negotiations and agree a final climate text.",
         leaf_icon, GREEN, 22, 62),
        ("GAZA · AID", "PEACE PLAN 'FALLING SHORT'",
         "Aid groups score the UN-backed Gaza plan 4 out of 26, as Israeli "
         "troops cross the ceasefire line in Nuseirat.",
         aid_icon, TEAL, 22, 62),
    ]
    for i, (kick, head, body, icon, accent, itop, ih) in enumerate(stories):
        x0 = M + i * (cw + 16)
        story_panel(x0, y0, x0 + cw, y1, kick, head, body, icon, accent, itop, ih)

    # ---- Bottom row: three panels ----
    y0, y1 = 732, 916
    stories2 = [
        ("DHAKA · UNREST", "UNREST SPREADS",
         "Yunus's home torched; violence hits 28 districts.",
         flame_icon, ORANGE, 10, 38),
        ("HORMUZ · ENERGY", "HORMUZ ON EDGE",
         "IEA warns of the worst energy threat yet; two missing.",
         drop_icon, NAVY, 10, 38),
        ("KYIV · WAR", "€45BN FOR KYIV",
         "EU proposes a huge Ukraine loan; Crimea bridge hit again.",
         bridge_icon, SLATE, 10, 38),
    ]
    for i, (kick, head, body, icon, accent, itop, ih) in enumerate(stories2):
        x0 = M + i * (cw + 16)
        story_panel(x0, y0, x0 + cw, y1, kick, head, body, icon, accent, itop, ih)

    # ---- Footer strip ----
    d.line([(M, 934), (W - M, 934)], fill=RULE, width=2)
    text_block(d, (M, 948),
               "ALSO ON 19 NOVEMBER:  A Van Gogh sells for a record $190.4m  ·  "
               "NASA's Voyager 1 passes one light-day  ·  Migrant boat sinks off "
               "Senegal  ·  Mongolia's president resigns.",
               font(FB, 20), INK, W - 2 * M, leading=27)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
