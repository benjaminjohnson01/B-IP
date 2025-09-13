#!/usr/bin/env python3

"""A command-line tool to compress and/or mute a video file using ffmpeg."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def out_path_for(src: Path, out_arg: Path | None, tag: str, ext: str) -> Path:
    if out_arg is None:
        return src.with_name(f"{src.stem}{tag}{ext}")
    o = out_arg.resolve()
    if o.exists() and o.is_dir():
        return o / f"{src.stem}{tag}{ext}"
    if o.suffix:  # looks like a file path with extension
        return o
    return o / f"{src.stem}{tag}{ext}"


def main() -> None:
    p = argparse.ArgumentParser(
        description="Create a single output: compress, mute, or both."
    )
    p.add_argument("video", type=Path, help="Path to the input video (e.g., .mov)")
    p.add_argument("-o", "--output", type=Path, help="Output file path OR directory")
    p.add_argument(
        "-m",
        "--mode",
        choices=["compress", "mute", "both"],
        default="compress",
        help="Operation to perform: compress, mute, or both (compress+mute)",
    )
    args = p.parse_args()

    if shutil.which("ffmpeg") is None:
        sys.exit("Error: ffmpeg not found. Please install ffmpeg and try again.")

    src = args.video.resolve()
    if not src.exists():
        sys.exit(f"Error: {src} not found.")

    # Decide tag + extension for default naming.
    tag = {"compress": "_c", "mute": "_m", "both": "_cm"}[args.mode]
    ext = ".mp4" if args.mode in {"compress", "both"} else src.suffix
    out = out_path_for(src, args.output, tag, ext)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Build the ffmpeg command based on mode (single output file).
    if args.mode == "compress":
        cmd = [
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
            str(out),
        ]
    elif args.mode == "mute":
        cmd = [
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
            str(out),
        ]
    else:  # both = compress + mute (compressed video, no audio)
        cmd = [
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
            "-an",
            str(out),
        ]

    subprocess.run(cmd, check=True)
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
