#!/usr/bin/env python3
"""Themed QR for Freya DNA Bet."""
import sys
from pathlib import Path

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont

URL = sys.argv[1] if len(sys.argv) > 1 else "https://k04l.github.io/freya-bet/"
OUT = Path(__file__).resolve().parent / "freya-qr.png"

# Deep plum + gold theme
DARK = (26, 20, 35)
GOLD = (232, 196, 104)
CREAM = (247, 240, 230)
LILAC = (155, 135, 199)

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    fill_color=GOLD,
    back_color=DARK,
).convert("RGBA")

# Pad for label banner
pad_top, pad_side, pad_bot = 72, 36, 96
w, h = img.size
canvas = Image.new("RGBA", (w + pad_side * 2, h + pad_top + pad_bot), DARK + (255,))
canvas.paste(img, (pad_side, pad_top), img)

draw = ImageDraw.Draw(canvas)
# Try a nice font; fall back to default
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

title = "Who's Freya?"
sub = "DNA breed bet · scan to guess"
ft, fs = font(36), font(18)
# Center title
tw = draw.textlength(title, font=ft)
draw.text(((canvas.width - tw) / 2, 18), title, fill=GOLD, font=ft)
sw = draw.textlength(sub, font=fs)
draw.text(((canvas.width - sw) / 2, canvas.height - 58), sub, fill=CREAM, font=fs)
# Accent dots
draw.ellipse((28, canvas.height - 52, 40, canvas.height - 40), fill=LILAC)
draw.ellipse((canvas.width - 40, canvas.height - 52, canvas.width - 28, canvas.height - 40), fill=LILAC)

canvas.convert("RGB").save(OUT, "PNG")
print(f"Wrote {OUT} → {URL}")
