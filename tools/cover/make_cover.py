"""Build the EPUB cover: real data from the book, in the book's own palette.

The visual is the message-length distribution of all 35,267 messages in the
chat fixture, which is the histogram a reader meets in Chapter 12. It is
genuinely right-skewed (peak at one word, tail to 116), so the shape is the
data's rather than a decoration, and it doubles as a sneak peek at what the
book actually does.

No SIUE marks and no AURA Lab logo: the 2026 brand policy bars units from
making their own, and the lab's logo system was retired. Typography plus data.
"""
import csv
import pathlib
import re
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2560
PAPER = (252, 251, 247)
INK = (25, 27, 30)
MUTED = (107, 99, 87)
RED = (196, 20, 37)
RULE = (224, 218, 206)

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"


def font(name, size, weight=None):
    f = ImageFont.truetype(str(FONTS / f"{name}.ttf"), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            try:
                f.set_variation_by_name(weight if isinstance(weight, str) else "Bold")
            except Exception:
                pass
    return f


# ---- data ---------------------------------------------------------------
rows = list(csv.DictReader(open(HERE / "twitch_chat_sample.csv", encoding="utf-8",
                                errors="replace")))
lengths = [len(re.findall(r"[A-Za-z']+", (r["message"] or ""))) for r in rows]
counts = Counter(lengths)
NBARS = 34
series = [counts.get(i, 0) for i in range(NBARS)]
peak = max(series)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- the histogram: a band across the lower half, bars rising from a baseline
base_y = int(H * 0.845)
# 0.45 puts the peak clear of the subtitle, which ends near y=854;
# 0.52 ran the tall bar up behind the text and 0.40 left a dead third.
band_h = int(H * 0.45)
left, right = 110, W - 110
gap = 7
bw = (right - left - gap * (NBARS - 1)) / NBARS
for i, v in enumerate(series):
    x0 = left + i * (bw + gap)
    h = (v / peak) * band_h
    # Deepen the leading bars, fade the tail, so the skew reads at thumbnail size.
    t = i / (NBARS - 1)
    col = tuple(int(RED[c] + (PAPER[c] - RED[c]) * (t ** 1.5) * 0.72) for c in range(3))
    d.rectangle([x0, base_y - h, x0 + bw, base_y], fill=col)

d.line([left, base_y, right, base_y], fill=INK, width=3)

# ---- type ---------------------------------------------------------------
title = font("Archivo", 190, 700)
sub = font("Newsreader", 52)
meta = font("Archivo", 44, 600)
small = font("Archivo", 38, 500)

y = 230
for line in ("Vibes to", "Variables"):
    d.text((110, y), line, font=title, fill=INK)
    y += 196

y += 34
d.line([110, y, 430, y], fill=RED, width=8)
y += 58

for line in ("A Methods Package for Students",
             "New to Research, Stats, and Code"):
    d.text((110, y), line, font=sub, fill=MUTED)
    y += 70

d.text((110, base_y + 92), "ALEX P. LEITH", font=meta, fill=INK)
d.text((110, base_y + 158), "THIRD EDITION", font=small, fill=RED)

cap = font("Newsreader", 34)
d.text((right, base_y + 96), "message length, 35,267 messages", font=cap, fill=MUTED,
       anchor="ra")
d.text((right, base_y + 146), "Twitch chat corpus, November 2018", font=cap, fill=MUTED,
       anchor="ra")

out = HERE / "cover.png"
img.save(out, "PNG")
print(f"wrote {out}  {out.stat().st_size/1024:.0f} KB  {W}x{H}")
