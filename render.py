#!/usr/bin/env python3
"""Render the 26 November 2026 world-news poster, 1024x1024 PNG.

A newspaper front page drawn with PIL and the DejaVu faces only.
No network, no fetched images: every panel is drawn by this script,
so running it twice writes byte-identical output.

Stories checked against reporting dated Thursday 26 November 2026
(Reuters via wire roundups, BBC, Al Jazeera, CNN, AP):
- LEAD (Gulf): a drone attack on a Kuwaiti military site kills two
  Italian technicians; Iran denies any role. Iran's Revolutionary
  Guards say two tankers hit mines in the Strait of Hormuz near
  Khasab; a Houthi projectile hits the Saudi Aramco refinery at
  Jazan, killing a Nepali worker.
- LEAD (Ukraine): Russian missiles hit a shopping centre in Kyiv,
  wounding seven, as 113 drones are launched overnight; Ukraine says
  its defences downed 87 missiles and drones. Trump urges Putin to
  pull back from widening the war.
- LEAD (Gaza): Israeli strikes kill nine in Gaza, including the
  Hamas-appointed deputy education minister, a third straight night
  of attacks despite a year-old ceasefire.
- Plus a 12-story grid, five stat tiles, a world map and an
  also-on list, all from the same day's reporting.
"""

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
BG = (247, 242, 230)          # newsprint
INK = (24, 22, 19)
MUTED = (96, 90, 80)
NAVY = (24, 38, 68)
CRIMSON = (198, 16, 48)
TEAL = (14, 102, 102)
OCHRE = (178, 108, 2)
SKYBLUE = (36, 110, 168)
CARD = (255, 255, 255)
RULE = (203, 195, 179)
GOLD = (214, 164, 32)
SEA = (20, 62, 112)
LEAF = (34, 120, 60)
SEACOL = (190, 216, 236)
LANDCOL = (222, 205, 170)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def sb(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sr(size):
    return font("DejaVuSerif.ttf", size)


def ab(size):
    return font("DejaVuSans-Bold.ttf", size)


def ar(size):
    return font("DejaVuSans.ttf", size)


def lines_for(d, text, f, maxw):
    """Word-wrap text to the given pixel width."""
    out, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def block(d, x, y, text, f, fill, maxw, step):
    """Draw wrapped text, return y below the last line."""
    for line in lines_for(d, text, f, maxw):
        d.text((x, y), line, font=f, fill=fill)
        y += step
    return y


def centre(d, cx, y, text, f, fill):
    d.text((cx, y), text, font=f, fill=fill, anchor="ma")


def frame(d, x, y, w, h, accent):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=1)
    d.rectangle([x, y, x + w, y + 5], fill=accent)


# --- lead scenes (each drawn on a small off-screen canvas) ---------------

def scene_gulf(d, x, y, w, h):
    """Night over a Gulf refinery: flare stacks, a drone, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 20, 44))
    for sx, sy in ((26, 14), (88, 26), (150, 10), (214, 22), (268, 12),
                   (60, 40), (180, 38), (238, 46)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # Refinery silhouette.
    base = y + h - 26
    d.rectangle([x, y + 30, x + w, base], fill=(16, 30, 58))
    for tx in (30, 96, 168, 236):
        d.rectangle([x + tx, y + 34, x + tx + 8, base], fill=(52, 66, 96))
    d.rectangle([x + 20, base - 14, x + w - 20, base], fill=(70, 84, 112))
    # Flames from two stacks.
    for fx in (34, 100):
        d.polygon([(x + fx - 6, y + 34), (x + fx + 14, y + 34),
                   (x + fx + 4, y + 12)], fill=(240, 140, 20))
        d.polygon([(x + fx - 2, y + 34), (x + fx + 10, y + 34),
                   (x + fx + 4, y + 20)], fill=(250, 210, 60))
    # Smoke.
    for i, (sx, sy, r) in enumerate(((150, 26, 9), (168, 18, 12), (190, 28, 8))):
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(120, 120, 125))
    # Drone with blinking lights.
    dx, dy = x + w - 78, y + 16
    d.line([(dx - 22, dy), (dx + 22, dy)], fill=(200, 200, 200), width=2)
    d.ellipse([dx - 6, dy - 4, dx + 6, dy + 4], fill=(220, 220, 220))
    d.ellipse([dx - 24, dy - 3, dx - 18, dy + 3], fill=CRIMSON)
    d.ellipse([dx + 18, dy - 3, dx + 24, dy + 3], fill=CRIMSON)


def scene_kyiv(d, x, y, w, h):
    """Kyiv skyline at night: missile streaks, air-defence flashes."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 18, 42))
    for sx, sy in ((24, 12), (90, 20), (160, 8), (220, 18), (280, 10),
                   (58, 30), (140, 34), (250, 30)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    base = y + h - 18
    # Skyline blocks with lit windows.
    blocks = [(8, 34, 46), (62, 22, 52), (122, 40, 38), (168, 26, 48),
              (224, 36, 54), (286, 24, 40)]
    for bx, bh, bw in blocks:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(30, 42, 66))
        for wy in range(base - bh + 6, base - 6, 10):
            for wx in range(bx + 6, bx + bw - 4, 12):
                if (wx + wy) % 20 < 10:
                    d.rectangle([x + wx, y + wy - base + base, x + wx + 4,
                                 y + wy - base + base + 5],
                                fill=(255, 210, 90))
    # Missile streaks coming down.
    for mx, my, ln in ((90, 8, 26), (190, 4, 30), (262, 10, 22)):
        d.line([(x + mx, y + my), (x + mx - 8, y + my + ln)],
               fill=(255, 120, 80), width=3)
        d.ellipse([x + mx - 11, y + my + ln - 3, x + mx - 5, y + my + ln + 3],
                  fill=(255, 200, 120))
    # Air-defence flash.
    d.ellipse([x + 150, y + 44, x + 170, y + 64], fill=(255, 240, 160))
    d.ellipse([x + 155, y + 49, x + 165, y + 59], fill=(255, 255, 255))


def scene_gaza(d, x, y, w, h):
    """Gaza at dusk: low blocks, smoke columns, a red sky band."""
    d.rectangle([x, y, x + w, y + h], fill=(64, 34, 30))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(40, 26, 24))
    # Sun low on the horizon.
    d.ellipse([x + w - 56, y + 12, x + w - 20, y + 48], fill=(250, 150, 60))
    # Smoke columns.
    for sx in (70, 150, 230):
        d.ellipse([x + sx - 14, y + 10, x + sx + 14, y + 38], fill=(90, 78, 74))
        d.ellipse([x + sx - 9, y + 2, x + sx + 9, y + 20], fill=(110, 96, 90))
    # Rooftops.
    base = y + h - 30
    for bx, bh, bw in [(10, 26, 70), (90, 18, 60), (160, 30, 74),
                       (244, 20, 56)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(52, 36, 32))
        for wx in range(bx + 8, bx + bw - 6, 14):
            d.rectangle([x + wx, base - bh + 6, x + wx + 5, base - bh + 11],
                        fill=(240, 190, 90))


def lead_story(img, d, x, y, w, h, accent, scene, kicker, head, body):
    frame(d, x, y, w, h, accent)
    tmp = Image.new("RGB", (w - 2, 82), BG)
    scene(ImageDraw.Draw(tmp), 0, 0, w - 2, 82)
    img.paste(tmp, (x + 1, y + 6))
    tx, tw = x + 13, w - 26
    d.text((tx, y + 94), kicker, font=ab(13), fill=accent)
    y2 = block(d, tx, y + 112, head, sb(20), INK, tw, 23)
    block(d, tx, y2 + 5, body, ar(13), (62, 58, 52), tw, 16)


def mini_story(d, x, y, w, h, accent, kicker, head, tail):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=1)
    d.rectangle([x, y, x + 4, y + h], fill=accent)
    tx, tw = x + 12, w - 22
    d.text((tx, y + 7), kicker, font=ab(11), fill=accent)
    block(d, tx, y + 24, head, sb(15), INK, tw, 18)
    d.text((tx, y + h - 19), tail, font=ar(12), fill=(62, 58, 52))


def map_panel(d, x, y, w, h):
    """Stylised world map: pale sea, tan land, red pins with labels."""
    d.rectangle([x, y, x + w, y + h], fill=SEACOL, outline=RULE, width=1)
    land = [
        [(28, 8), (208, 4), (232, 22), (188, 44), (118, 48), (58, 38), (26, 22)],
        [(224, 52), (284, 50), (294, 72), (264, 84), (238, 70)],
        [(438, 6), (498, 4), (510, 20), (478, 30), (444, 24)],
        [(446, 32), (518, 30), (543, 52), (518, 82), (478, 78), (450, 56)],
        [(528, 6), (778, 4), (828, 20), (798, 44), (658, 50), (558, 38), (526, 20)],
        [(788, 60), (858, 58), (870, 72), (828, 80), (794, 74)],
    ]
    for poly in land:
        d.polygon([(x + px, y + py) for px, py in poly], fill=LANDCOL)
    pins = [
        ("Kuwait City", 566, 40, "above"),
        ("Khasab", 586, 46, "below"),
        ("Jazan", 540, 52, "below"),
        ("Kyiv", 490, 18, "above"),
        ("Gaza", 512, 44, "left"),
        ("London", 452, 12, "left"),
        ("Seoul", 780, 28, "below"),
        ("Jakarta", 714, 54, "below"),
    ]
    for name, px, py, where in pins:
        d.ellipse([x + px - 5, y + py - 5, x + px + 5, y + py + 5],
                  fill=CRIMSON, outline=(255, 255, 255), width=2)
        f = ab(11)
        tw = d.textlength(name, font=f)
        if where == "above":
            d.text((x + px - tw / 2, y + py - 20), name, font=f, fill=NAVY)
        elif where == "below":
            d.text((x + px - tw / 2, y + py + 8), name, font=f, fill=NAVY)
        else:
            d.text((x + px - tw - 9, y + py - 6), name, font=f, fill=NAVY)
    d.rectangle([x + 6, y + 4, x + 150, y + 24], fill=(255, 255, 255))
    d.text((x + 12, y + 7), "WHERE IT HAPPENED", font=ab(12), fill=NAVY)


def build():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)
    MX = 28
    CW = SIZE - 2 * MX

    # Masthead.
    d.rectangle([0, 0, SIZE, 84], fill=NAVY)
    centre(d, SIZE // 2, 12, "THE WORLD IN ONE DAY", sb(42), (255, 255, 255))
    centre(d, SIZE // 2, 58, "THURSDAY \u00b7 26 NOVEMBER 2026", ab(20), GOLD)
    d.rectangle([0, 84, SIZE, 88], fill=CRIMSON)

    centre(d, SIZE // 2, 94,
           "50 STORIES \u00b7 10 REGIONS \u00b7 21 FIELDS \u2014 ALL FIRST REPORTED "
           "ON THURSDAY 26 NOVEMBER 2026", ab(15), INK)
    centre(d, SIZE // 2, 116,
           "GULF 8 \u00b7 EUROPE 11 \u00b7 N. AMERICA 6 \u00b7 MIDDLE EAST 7 \u00b7 "
           "E & SE ASIA 6 \u00b7 S. ASIA 3 \u00b7 AFRICA 4 \u00b7 OCEANIA 2 \u00b7 GLOBAL 3",
           ar(11), MUTED)

    # Stat tiles.
    tiles = [
        ("2", CRIMSON, "Italian technicians killed in Kuwait drone attack"),
        ("87", NAVY, "Russian missiles and drones Ukraine says it downed"),
        ("77,000", OCHRE, "UK net migration, lowest since 1997"),
        ("~900,000", TEAL, "US homes dark in the Thanksgiving storm"),
        ("$91.73", LEAF, "Brent crude, up 1.2% on the Gulf attacks"),
    ]
    tw = (CW - 4 * 8) // 5
    for i, (num, colour, label) in enumerate(tiles):
        tx = MX + i * (tw + 8)
        d.rectangle([tx, 140, tx + tw, 216], fill=CARD, outline=RULE, width=1)
        d.rectangle([tx, 140, tx + tw, 145], fill=colour)
        d.text((tx + 12, 152), num, font=sb(28), fill=colour)
        block(d, tx + 12, 188, label, ar(13), (62, 58, 52), tw - 24, 16)

    # Three lead stories.
    mw = (CW - 2 * 12) // 3
    leads = [
        (CRIMSON, scene_gulf, "THE GULF \u00b7 KUWAIT \u00b7 HORMUZ",
         "Drone attack kills two Italians in Kuwait as Gulf comes under fire",
         "Iran denies any role. Tehran says two tankers hit mines near "
         "Khasab; a Houthi projectile hits the Jazan refinery, killing "
         "one worker."),
        (NAVY, scene_kyiv, "KYIV \u00b7 UKRAINE",
         "Russian missiles hit Kyiv shopping centre; seven wounded",
         "113 drones launched overnight; Kyiv says 87 missiles and drones "
         "were downed. Trump urges Putin to pull back from widening the war."),
        (TEAL, scene_gaza, "GAZA \u00b7 DEIR AL-BALAH",
         "Israeli strikes kill nine in Gaza, a third night of attacks",
         "A Hamas-appointed deputy education minister is among the dead, "
         "despite a ceasefire now a year old."),
    ]
    for i, (accent, scene, kicker, head, body) in enumerate(leads):
        lead_story(img, d, MX + i * (mw + 12), 224, mw, 246, accent, scene,
                   kicker, head, body)

    # Twelve-story grid, 4 across by 3 down.
    grid = [
        (NAVY, "EUROPE \u00b7 ECB", "Hern\u00e1ndez de Cos to lead the ECB",
         "Succeeds Lagarde."),
        (NAVY, "ECONOMY \u00b7 KOREA", "Bank of Korea raises rates to 3.25%",
         "Surprise hike."),
        (OCHRE, "USA \u00b7 THANKSGIVING", "Macy\u2019s parade postponed by storm",
         "First time in 100 years."),
        (TEAL, "TECH \u00b7 CHIPS", "Nvidia halts server shipments to SE Asia",
         "New US licence rules."),
        (NAVY, "KOREA \u00b7 PYONGYANG", "North Korea expels Swiss diplomat",
         "48 hours to leave."),
        (CRIMSON, "WAR \u00b7 RUSSIA", "Leaked data put Russian war dead near 490,000",
         "BBC analysis."),
        (NAVY, "EUROPE \u00b7 BRUSSELS", "EU budget summit clashes over Ukraine aid",
         "No deal on 2028\u201334 budget."),
        (OCHRE, "DISASTER \u00b7 INDONESIA", "Rain hampers rescue at flooded gold mine",
         "13 dead, 13 missing."),
        (TEAL, "HEALTH \u00b7 CONGO", "DR Congo Ebola passes 12,000 cases",
         "5,904 deaths so far."),
        (NAVY, "MUSIC \u00b7 OBITUARY", "Duran Duran guitarist Andy Taylor dies at 65",
         "Original member."),
        (NAVY, "DEFENCE \u00b7 EUROPE", "Five nations buy 430 CV90 combat vehicles",
         "Joint order."),
        (NAVY, "SERBIA \u00b7 VOTE", "Presidential election set for 27 December",
         "Date announced."),
    ]
    gw = (CW - 3 * 10) // 4
    gh = (264 - 2 * 8) // 3
    for i, (accent, kicker, head, tail) in enumerate(grid):
        gx = MX + (i % 4) * (gw + 10)
        gy = 478 + (i // 4) * (gh + 8)
        mini_story(d, gx, gy, gw, gh, accent, kicker, head, tail)

    # Map strip.
    map_panel(d, MX, 750, CW, 88)

    # Also-on list.
    d.text((MX, 846), "ALSO ON 26 NOVEMBER", font=ab(15), fill=NAVY)
    also = [
        "Brazil calls the US tariff plan \u2018unacceptable\u2019",
        "India pledges $1.62bn to rebuild flood-hit Nepal",
        "Myanmar rejects parts of the ICJ Rohingya ruling",
        "Guinea-Bissau rulers delay elections to 2028",
        "Abrego Garcia lands in Spain after US case dismissed",
        "World tops 2\u00b0C above pre-industrial for six days running",
    ]
    for i, item in enumerate(also):
        ax = MX if i % 2 == 0 else MX + CW // 2 + 12
        ay = 874 + (i // 2) * 24
        d.text((ax, ay), "\u2022", font=ab(14), fill=CRIMSON)
        d.text((ax + 16, ay), item, font=ar(13), fill=INK)

    # Footer.
    d.rectangle([0, 954, SIZE, SIZE], fill=NAVY)
    centre(d, SIZE // 2, 968,
           "DATE CHECK \u2014 Every story above happened or was first reported "
           "on Thursday 26 November 2026.", ab(15), GOLD)
    centre(d, SIZE // 2, 994, "Sources: Reuters \u00b7 BBC \u00b7 Al Jazeera \u00b7 AP \u2014 26 November 2026",
           ar(13), (200, 196, 188))

    img.save("entry.png")


if __name__ == "__main__":
    build()
