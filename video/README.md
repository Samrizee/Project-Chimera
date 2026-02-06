# video/README.md

This folder contains a small Python script to generate a short MP4 video made of text slides.

Prerequisites
- Python 3.8+
- ffmpeg installed and on PATH (install via your OS package manager or from https://ffmpeg.org)

Install Python dependencies (prefer a virtualenv):

```bash
python3 -m pip install --upgrade pip
python3 -m pip install moviepy pillow imageio-ffmpeg
```

Create the video:

```bash
python3 video/make_video.py
```

Output
- `video/output/output.mp4`

Notes
- The script uses Pillow to render text to images (avoiding ImageMagick).
- Adjust slide text and `DURATION` in `video/make_video.py` as needed.
