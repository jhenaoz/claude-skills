#!/usr/bin/env python3
"""Download YouTube videos as MP4 files."""

import argparse
import os
import re
import sys

import yt_dlp


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


QUALITY_MAP = {
    "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "1080": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[height<=1080]",
    "720": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]",
    "480": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[height<=480]",
    "360": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best[height<=360]",
}


def list_formats(url: str) -> None:
    """List available formats for a YouTube video."""
    ydl_opts = {"listformats": True, "quiet": False}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def _progress_hook(d: dict) -> None:
    """Print download progress to stderr."""
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "N/A")
        speed = d.get("_speed_str", "N/A")
        print(f"\rDownloading: {percent} at {speed}", end="", file=sys.stderr)
    elif d["status"] == "finished":
        print("\nDownload complete, processing...", file=sys.stderr)


def download_video(url: str, output_path: str, quality: str = "best") -> str:
    """Download a YouTube video and return the final file path."""
    format_str = QUALITY_MAP.get(quality, QUALITY_MAP["best"])

    ydl_opts = {
        "format": format_str,
        "outtmpl": output_path,
        "merge_output_format": "mp4",
        "progress_hooks": [_progress_hook],
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos as MP4")
    parser.add_argument("url", help="YouTube video URL or ID")
    parser.add_argument("-o", "--output", help="Output file path (default: title-based in current directory)")
    parser.add_argument("-q", "--quality", default="best", choices=list(QUALITY_MAP.keys()),
                        help="Video quality (default: best)")
    parser.add_argument("--list-formats", action="store_true", help="List available formats and exit")
    args = parser.parse_args()

    if args.list_formats:
        list_formats(args.url)
        return

    video_id = extract_video_id(args.url)
    original_cwd = os.environ.get("ORIGINAL_CWD", os.getcwd())

    if args.output:
        output_path = args.output if os.path.isabs(args.output) else os.path.join(original_cwd, args.output)
    else:
        output_path = os.path.join(original_cwd, "%(title)s [%(id)s].%(ext)s")

    print(f"Downloading video: {video_id} (quality: {args.quality})", file=sys.stderr)
    final_path = download_video(args.url, output_path, args.quality)

    print(f"Video saved to: {final_path}", file=sys.stderr)
    print(final_path)


if __name__ == "__main__":
    main()
