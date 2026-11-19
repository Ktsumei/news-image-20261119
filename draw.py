#!/usr/bin/env python3
"""Draw the 19 Nov 2026 world-news front page, 1024x1024, deterministic.
No network, no randomness. Run from this directory: it writes entry.png
beside this script. Fonts: DejaVu (system). All stories are events that
happened, or were first reported, on Thursday 19 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

SERIF_B = lambda s: load("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: load("DejaVuSans.ttf", s)
SANS_B = lambda s: load("DejaVuSans-Bold.ttf", s)

W, H = 1024, 1024
NAVY = (13, 38, 68)
RED = (178, 34, 34)
INK = (18, 18, 18)
GREY = (96, 96, 96)
LIGHT = (240, 243, 246)
RULE = (205, 205, 205)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

def lines_for(text, fnt, max_w):
    words = text.split()
    out, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out

def block(x, y, text, fnt, max_w, leading, color=INK):
    for ln in lines_for(text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y

# --- Masthead ---------------------------------------------------------------
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((32, 22), "THE WORLD IN ONE DAY", font=SERIF_B(58), fill="white")
d.text((32, 100), "THURSDAY 19 NOVEMBER 2026  \u2022  THE DAY'S WORLD NEWS IN ONE IMAGE",
       font=SANS_B(21), fill=(255, 210, 90))

# --- Lead story: the Shenzhen summit ---------------------------------------
y = 168
d.rectangle([32, y, 42, y + 8], fill=RED)
d.text((56, y - 6), "LEAD  \u2014  SHENZHEN", font=SANS_B(20), fill=RED)
y += 34
d.text((32, y), "TRUMP, XI AND PUTIN", font=SERIF_B(40), fill=INK)
y += 48
d.text((32, y), "MEET FACE TO FACE", font=SERIF_B(40), fill=INK)
y += 56
y = block(32, y,
    "Donald Trump, Xi Jinping and Vladimir Putin meet in Shenzhen today in the "
    "first three-way summit of the leaders of the world's three largest nuclear "
    "powers. Nuclear arms and the Iran war top the agenda; Ukraine is off it.",
    SANS(22), 960, 28)
d.line([32, y + 12, 992, y + 12], fill=RULE, width=2)

# --- Six stories in a 2 x 3 grid -------------------------------------------
stories = [
    ("CULTURE", (140, 40, 90), "GTA VI ROLLS OUT WORLDWIDE",
     "After 13 years, Rockstar's Grand Theft Auto VI unlocks at midnight today in "
     "each market, starting in New Zealand. Critics gave it 99 on Metacritic; "
     "pre-orders passed $1.65 billion."),
    ("WEATHER", (0, 110, 130), "CYCLONE AKVAN BEARS DOWN ON INDIA",
     "Cyclone Akvan is set to cross India's east coast between Machilipatnam and "
     "Puri, bringing heavy rain and strong winds."),
    ("DIPLOMACY", (15, 90, 140), "CANADA RECALIBRATES CHINA TIES",
     "Prime Minister Mark Carney says Canada is adjusting its ties with China, "
     "aiming to strike the right deal with the United States."),
    ("TECH", (120, 70, 140), "SENATORS WARN AI CYBER THREATS OUTPACE DEFENCES",
     "US senators warn the White House that AI-enabled cyber threats are "
     "outpacing America's defences, and urge faster action."),
    ("SCIENCE", (0, 120, 90), "NASA CONFIRMS VOYAGER 1 ONE LIGHT-DAY AWAY",
     "NASA confirms Voyager 1, launched in 1977, is now one light-day from Earth "
     "\u2014 about 16 billion miles. A radio signal takes a full day to reach it."),
    ("THE GULF", (178, 34, 34), "SAUDI ARABIA: DANGER HAS PASSED",
     "Saudi Arabia says the danger has passed in three southern cities after "
     "alerts, as the Gulf calms following days of strikes."),
]
grid_top = y + 28
cell_w, cell_h = 480, 160
for i, (tag, color, head, body) in enumerate(stories):
    col, row = i % 2, i // 2
    x = 32 if col == 0 else 512
    yy = grid_top + row * cell_h
    d.rectangle([x, yy, x + 6, yy + 18], fill=color)
    d.text((x + 16, yy - 2), tag, font=SANS_B(17), fill=color)
    yy2 = yy + 24
    for ln in lines_for(head, SERIF_B(23), cell_w - 16):
        d.text((x, yy2), ln, font=SERIF_B(23), fill=INK)
        yy2 += 28
    block(x, yy2 + 2, body, SANS(18), cell_w - 16, 24)

# --- Also on 19 November ----------------------------------------------------
strip_y = grid_top + 3 * cell_h + 8
d.rectangle([0, strip_y, W, strip_y + 64], fill=LIGHT)
d.text((32, strip_y + 8), "ALSO ON 19 NOVEMBER", font=SANS_B(18), fill=NAVY)
block(32, strip_y + 32,
    "M\u00e9lenchon could win in France  \u2022  "
    "Cocaine and pills seized in Libya  \u2022  "
    "India-Japan defence talks  \u2022  Oil prices fall",
    SANS(16), 960, 20)

# --- Footer -----------------------------------------------------------------
d.text((32, 992),
       "Sources: Reuters  \u2022  AP  \u2022  BBC  \u2022  NASA  \u2022  The Hindu      "
       "Events of 19 November 2026, in any time zone",
       font=SANS(16), fill=GREY)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(OUT, os.path.getsize(OUT), img.size)
