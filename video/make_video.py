#!/usr/bin/env python3
"""Generate a short MP4 video composed of text slides.

Usage:
  python3 video/make_video.py

Dependencies:
  pip install moviepy pillow imageio-ffmpeg

The script creates `video/output/output.mp4`.
"""
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np


slides = [
    "Spec Kit — Spec-Driven Development",
    "Supports multiple AI agents",
    "Generates agent-specific command files",
    "Includes templates and scripts",
    "Create, run, and extend"
]

OUT_DIR = os.path.join("video", "output")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1280, 720
DURATION = 3  # seconds per slide

def make_image_for_text(text, index):
    bg_colors = [(18, 52, 86), (34, 68, 102), (50, 84, 118), (66,100,134), (82,116,150)]
    bg = bg_colors[index % len(bg_colors)]
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except Exception:
        font = ImageFont.load_default()

    # Simple word-wrapping
    max_width = W - 120
    words = text.split()
    lines = []
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if draw.textsize(test, font=font)[0] <= max_width:
            line = test
        else:
            lines.append(line)
            line = w
    lines.append(line)

    total_h = sum(draw.textsize(l, font=font)[1] for l in lines) + (len(lines)-1) * 10
    y = (H - total_h) // 2
    for l in lines:
        lw, lh = draw.textsize(l, font=font)
        draw.text(((W - lw) // 2, y), l, font=font, fill=(255, 255, 255))
        y += lh + 10
    return img


def main():
    clips = []
    for i, s in enumerate(slides):
        img = make_image_for_text(s, i)
        arr = np.array(img)
        clip = ImageClip(arr).set_duration(DURATION)
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose")
    out_path = os.path.join(OUT_DIR, "output.mp4")
    final.write_videofile(out_path, fps=24, codec="libx264", audio=False)
    print("Wrote:", out_path)


if __name__ == "__main__":
    main()
