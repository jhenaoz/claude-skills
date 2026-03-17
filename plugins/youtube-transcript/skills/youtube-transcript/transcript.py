#!/usr/bin/env python3
"""Download YouTube video transcript and save it as a text file."""

import argparse
import os
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi


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


def list_languages(video_id: str) -> list[dict]:
    """List available transcript languages for a video."""
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    return [
        {"code": t.language_code, "name": t.language, "is_generated": t.is_generated}
        for t in transcript_list
    ]


def fetch_transcript(video_id: str, languages: list[str] | None = None) -> tuple[str, str]:
    """Fetch transcript and return (formatted_text, language_code).

    Tries the requested languages in order, then falls back to any available transcript.
    """
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    if languages:
        try:
            found = transcript_list.find_transcript(languages)
            transcript = found.fetch()
            return _format_transcript(transcript), found.language_code
        except Exception:
            pass

    # Fallback: use whatever is available
    for t in transcript_list:
        transcript = t.fetch()
        print(f"Using available transcript: {t.language} ({t.language_code})", file=sys.stderr)
        return _format_transcript(transcript), t.language_code

    raise RuntimeError(f"No transcript available for video {video_id}")


def _format_transcript(transcript) -> str:
    lines = []
    for entry in transcript:
        minutes = int(entry.start // 60)
        seconds = int(entry.start % 60)
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        lines.append(f"{timestamp} {entry.text}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Download YouTube video transcript")
    parser.add_argument("url", help="YouTube video URL or ID")
    parser.add_argument("-o", "--output", help="Output file path (default: transcript_<id>.txt)")
    parser.add_argument("-l", "--language", default="en,es", help="Comma-separated language codes in priority order (default: en,es)")
    parser.add_argument("--list-languages", action="store_true", help="List available transcript languages and exit")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)

    if args.list_languages:
        langs = list_languages(video_id)
        for lang in langs:
            kind = "auto-generated" if lang["is_generated"] else "manual"
            print(f"  {lang['code']:>5s}  {lang['name']} ({kind})")
        return

    languages = [l.strip() for l in args.language.split(",")]
    # Use ORIGINAL_CWD to write output relative to the caller's directory
    original_cwd = os.environ.get("ORIGINAL_CWD", os.getcwd())
    default_output = os.path.join(original_cwd, f"transcript_{video_id}.txt")
    output_file = args.output if args.output else default_output

    print(f"Fetching transcript for video: {video_id}", file=sys.stderr)
    text, lang_code = fetch_transcript(video_id, languages)

    with open(output_file, "w") as f:
        f.write(text)

    print(f"Transcript ({lang_code}) saved to: {output_file}", file=sys.stderr)
    print(f"Lines: {len(text.splitlines())}", file=sys.stderr)
    # Print file path to stdout for the skill to capture
    print(output_file)


if __name__ == "__main__":
    main()
