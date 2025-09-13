#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser(description="Compress and mute a video.")
    p.add_argument("video", type=Path, help="Path to the input video (e.g., .mov)")
    args = p.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("Error: ffmpeg not found. Please install ffmpeg and try again.")

    src = args.video.resolve()
    if not src.exists():
        sys.exit(f"Error: {src} not found.")

    stem = src.stem
    out_dir = src.parent
    compressed = out_dir / f"{stem}_compressed.mp4"
    muted = out_dir / f"{stem}_muted{src.suffix}"

    # 1) Compress: H.264 with a sane CRF; keeps resolution, trims size significantly.
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(src),
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "23",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            str(compressed),
        ],
        check=True,
    )

    # 2) Remove sound: copy video stream, drop audio.
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(src),
            "-c",
            "copy",
            "-an",
            str(muted),
        ],
        check=True,
    )

    print(f"Wrote:\n  {compressed}\n  {muted}")


if __name__ == "__main__":
    main()
