#!/usr/bin/env python3
"""Render a Teams-style name label PNG.

Victor's clips are Microsoft Teams screen-share recordings, so they carry Teams'
own name labels burned in. Samiran's clips are bare webcam, so we recreate the
same labels to keep all three speakers looking like one recording.

Geometry and colours were measured from a frame of Victor's recording:
  tile label  226x26 purple pill, centred under the webcam tile
  speaker bar 246x26 purple pill, bottom-left of the frame

Usage: make_label.py "Samiran Shrestha" out.png [width]
"""

import sys

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
BG = (99, 99, 163, 255)
FG = (255, 255, 255, 255)
HEIGHT = 26
RADIUS = 6


def render(text: str, out_path: str, width: int = 226) -> None:
    img = Image.new("RGBA", (width, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, width - 1, HEIGHT - 1], radius=RADIUS, fill=BG)

    font = ImageFont.truetype(FONT_PATH, 15)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    draw.text(
        ((width - (right - left)) / 2 - left, (HEIGHT - (bottom - top)) / 2 - top),
        text,
        font=font,
        fill=FG,
    )
    img.save(out_path)


if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    render(name, out, int(sys.argv[3]) if len(sys.argv) > 3 else 226)
