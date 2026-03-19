---
name: youtube-download
description: Download a YouTube video as an MP4 file given its URL. Use when the user wants to download, save, or grab a video from YouTube.
argument-hint: <youtube-url> [--quality best|1080|720|480|360] [--output file.mp4]
allowed-tools: Bash, Read
---

# YouTube Video Downloader

Download YouTube videos as MP4 files.

## Prerequisites

- [ffmpeg](https://ffmpeg.org/) must be installed for merging video+audio streams. Install with: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux).

## How to use

Run the downloader from the skill directory using `uv`:

```bash
export ORIGINAL_CWD=$(pwd) && cd ${CLAUDE_SKILL_DIR} && uv run python download.py "$0"
```

- `$0` is the YouTube video URL provided by the user
- If the user specifies a quality, pass it with `-q`: `export ORIGINAL_CWD=$(pwd) && cd ${CLAUDE_SKILL_DIR} && uv run python download.py "$0" -q <quality>`
- If the user specifies an output file, pass it with `-o`: `export ORIGINAL_CWD=$(pwd) && cd ${CLAUDE_SKILL_DIR} && uv run python download.py "$0" -o <filename>`
- To list available formats: `export ORIGINAL_CWD=$(pwd) && cd ${CLAUDE_SKILL_DIR} && uv run python download.py "$0" --list-formats`
- Available qualities: `best`, `1080`, `720`, `480`, `360`

## After downloading

1. Tell the user the file path where the video was saved
2. Warn the user if the file is large
