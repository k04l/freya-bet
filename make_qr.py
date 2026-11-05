#!/usr/bin/env python3
"""Themed QR for Freya DNA Bet — gold modules on plum background."""
import sys
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont

URL = sys.argv[1] if len(sys.argv) > 1 else "https://k04l.github.io/freya-bet/"
OUT = Path(__file__).resolve().parent / "freya-qr.png"

DARK = (26, 20, 35)
GOLD = (232, 196, 104)
CREAM = (247, 240, 230)
LILAC = (155, 135, 199)

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=14, border=2)
qr.add_data(URL)
qr.make(fit=True)
# Build matrix manually so we control colors (StyledPilImage ignores fill on some versions)
matrix = qr.get_matrix()
n = len(matrix)
scale = 14
img = Image.new("RGB", (n * scale, n * scale), DARK)
px = img.load()
for y, row in enumerate(matrix):
    for x, cell in enumerate(row):
        if cell:
            for dy in range(scale):
                for dx in range(scale):
                    # soft rounded look: skip outer corners of each module
                    if (dx == 0 or dx == scale - 1) and (dy == 0 or dy == scale - 1):
                        continue
                    px[x * scale + dx, y * scale + dy] = GOLD

pad_top, pad_side, pad_bot = 78, 40, 100
w, h = img.size
canvas = Image.new("RGB", (w + pad_side * 2, h + pad_top + pad_bot), DARK)
canvas.paste(img, (pad_side, pad_top))
draw = ImageDraw.Draw(canvas)

def font(size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()

title, sub = "Who's Freya?", "DNA breed bet · scan to guess"
ft, fs = font(38), font(18)
tw = draw.textlength(title, font=ft)
draw.text(((canvas.width - tw) / 2, 20), title, fill=GOLD, font=ft)
sw = draw.textlength(sub, font=fs)
draw.text(((canvas.width - sw) / 2, canvas.height - 62), sub, fill=CREAM, font=fs)
draw.ellipse((30, canvas.height - 56, 42, canvas.height - 44), fill=LILAC)
draw.ellipse((canvas.width - 42, canvas.height - 56, canvas.width - 30, canvas.height - 44), fill=LILAC)
canvas.save(OUT, "PNG")
print(f"Wrote {OUT} → {URL}")
