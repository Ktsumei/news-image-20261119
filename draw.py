#!/usr/bin/env python3
"""Draw the front page for Thursday 19 November 2026.

This script renders one 1024 by 1024 PNG that sums up the day's world news.
It uses Pillow and the DejaVu typefaces that ship with the system. There is
no network access and no randomness, so every run produces the same bytes.
Run it from this directory; it writes entry.png next to itself.
"""

from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

OUTPUT = Path(__file__).resolve().parent / "entry.png"
TYPE_DIR = Path("/usr/share/fonts/truetype/dejavu")

PAGE = (1024, 1024)
EDGE = 32
COLUMN_GAP = 56

NAVY = (12, 36, 66)
CRIMSON = (172, 32, 32)
TEAL = (14, 92, 96)
PLUM = (112, 44, 96)
FOREST = (28, 110, 68)
CHARCOAL = (26, 26, 26)
MIDGREY = (110, 110, 110)
PALE = (240, 243, 247)
AMBER = (255, 205, 80)
HAIRLINE = (205, 205, 200)


class FrontPage:
    """Canvas plus the small helpers a newspaper page needs."""

    def __init__(self):
        self.img = Image.new("RGB", PAGE, "white")
        self.draw = ImageDraw.Draw(self.img)

    def face(self, filename, size):
        return ImageFont.truetype(str(TYPE_DIR / filename), size)

    def serif_b(self, size):
        return self.face("DejaVuSerif-Bold.ttf", size)

    def sans(self, size):
        return self.face("DejaVuSans.ttf", size)

    def sans_b(self, size):
        return self.face("DejaVuSans-Bold.ttf", size)

    def fit_lines(self, text, font, max_width):
        """Break text into lines no wider than max_width pixels."""
        words = text.split()
        lines = []
        current = ""
        for word in words:
            candidate = (current + " " + word).strip()
            if self.draw.textlength(candidate, font=font) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def paragraph(self, x, y, text, font, max_width, leading, fill=CHARCOAL):
        """Draw wrapped text; return the y coordinate just below it."""
        for line in self.fit_lines(text, font, max_width):
            self.draw.text((x, y), line, font=font, fill=fill)
            y += leading
        return y

    def kicker(self, x, y, label, color):
        """A small coloured bar followed by an uppercase label."""
        self.draw.rectangle([x, y + 2, x + 10, y + 16], fill=color)
        self.draw.text((x + 18, y - 2), label, font=self.sans_b(18), fill=color)
        return y + 26

    def story(self, x, y, width, tag, tag_color, headline, body):
        """One story: kicker, headline, body. Returns the y below it."""
        y = self.kicker(x, y, tag, tag_color)
        y = self.paragraph(x, y, headline, self.sans_b(21), width, 26)
        y = self.paragraph(x, y + 6, body, self.sans(17), width, 22)
        return y

    def masthead(self):
        self.draw.rectangle([0, 0, PAGE[0], 140], fill=NAVY)
        self.draw.text((EDGE, 20), "THE WORLD IN ONE DAY", font=self.serif_b(54), fill="white")
        self.draw.text(
            (EDGE, 96),
            "THURSDAY 19 NOVEMBER 2026  \u2022  THE DAY'S WORLD NEWS IN ONE IMAGE",
            font=self.sans_b(19),
            fill=AMBER,
        )

    def lead(self):
        y = 158
        y = self.kicker(EDGE, y, "LEAD  \u2014  SHENZHEN", CRIMSON)
        y = self.paragraph(
            EDGE, y,
            "Trump, Xi and Putin sit down together for the first time in Shenzhen",
            self.sans_b(33), PAGE[0] - 2 * EDGE, 40,
        )
        y = self.paragraph(
            EDGE, y + 10,
            "The three leaders open a first-ever trilateral summit in Shenzhen, with "
            "nuclear weapons and the war in Iran at the top of the agenda. Ukraine "
            "is kept off the table.",
            self.sans(20), PAGE[0] - 2 * EDGE, 27,
        )
        return y

    def grid(self, top):
        col_w = (PAGE[0] - 2 * EDGE - COLUMN_GAP) // 2
        left = EDGE
        right = EDGE + col_w + COLUMN_GAP
        pairs = [
            (
                ("GAMES", TEAL, "GTA VI opens worldwide to a 99 on Metacritic",
                 "It unlocks at midnight in each market, New Zealand first, "
                 "after $1.65 billion in pre-orders."),
                ("WEATHER", PLUM, "Cyclone Akvan bears down on India's east coast",
                 "The storm is set to cross the coast between Machilipatnam and Puri."),
            ),
            (
                ("DIPLOMACY", NAVY, "Carney recalibrates Canada's ties with China",
                 "Prime Minister Mark Carney leads a recalibration of the "
                 "relationship with Beijing."),
                ("TECHNOLOGY", CRIMSON, "Senators warn AI cyber threats outpace defences",
                 "US lawmakers say AI-powered attacks are moving faster than the "
                 "defences built to stop them."),
            ),
            (
                ("SPACE", FOREST, "Voyager 1 is one light-day from home, NASA confirms",
                 "The agency confirms on 19 November that the probe has reached "
                 "one light-day from Earth."),
                ("THE GULF", TEAL, "Saudi Arabia says the danger has passed",
                 "Authorities say the threat to three southern cities is over."),
            ),
        ]
        y = top
        for left_story, right_story in pairs:
            bottom_left = self.story(left, y, col_w, *left_story)
            bottom_right = self.story(right, y, col_w, *right_story)
            y = max(bottom_left, bottom_right) + 28
        return y

    def also(self, top):
        self.draw.rectangle([0, top, PAGE[0], top + 92], fill=PALE)
        self.draw.text((EDGE, top + 12), "ALSO ON 19 NOVEMBER", font=self.sans_b(18), fill=NAVY)
        items = (
            "M\u00e9lenchon could win in France  \u2022  Drug seizure in Libya  "
            "\u2022  India\u2013Japan talks  \u2022  Oil prices fall"
        )
        self.paragraph(EDGE, top + 44, items, self.sans(17), PAGE[0] - 2 * EDGE, 24)
        return top + 92

    def footer(self, top):
        self.draw.line([(EDGE, top), (PAGE[0] - EDGE, top)], fill=HAIRLINE, width=1)
        left = "THURSDAY 19 NOVEMBER 2026"
        right = "THE WORLD IN ONE DAY"
        self.draw.text((EDGE, top + 14), left, font=self.sans_b(15), fill=MIDGREY)
        w = self.draw.textlength(right, font=self.sans_b(15))
        self.draw.text((PAGE[0] - EDGE - w, top + 14), right, font=self.sans_b(15), fill=MIDGREY)


def main():
    page = FrontPage()
    page.masthead()
    bottom = page.lead()
    page.draw.line(
        [(EDGE, bottom + 14), (PAGE[0] - EDGE, bottom + 14)], fill=HAIRLINE, width=1
    )
    grid_bottom = page.grid(bottom + 32)
    also_bottom = page.also(grid_bottom + 16)
    page.footer(also_bottom + 18)
    page.img.save(OUTPUT, format="PNG")


if __name__ == "__main__":
    main()
