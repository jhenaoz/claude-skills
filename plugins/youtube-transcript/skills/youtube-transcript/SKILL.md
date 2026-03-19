---
name: youtube-transcript
description: Download a YouTube video transcript given its URL. Use when the user wants to get, fetch, or download a transcript or subtitles from a YouTube video.
argument-hint: <youtube-url> [--language en,es] [--output file.txt]
allowed-tools: Bash(uv run python transcript.py:*)
---

# YouTube Transcript Downloader

Download the transcript/subtitles from a YouTube video and save it as a text file.

## How to use

Run the transcript downloader from the skill directory using `uv`:

```bash
export ORIGINAL_CWD=$(pwd) && cd ${CLAUDE_SKILL_DIR} && uv run python transcript.py "$0"
```

- `$0` is the YouTube video URL provided by the user
- If the user specifies a language, pass it with `-l`: `export ORIGINAL_CWD=$(pwd) && cd ${CLAUDE_SKILL_DIR} && uv run python transcript.py "$0" -l <language_codes>`
- If the user specifies an output file, pass it with `-o`: `export ORIGINAL_CWD=$(pwd) && cd ${CLAUDE_SKILL_DIR} && uv run python transcript.py "$0" -o <filename>`
- Default language priority is `en,es` (English first, then Spanish)
- To list available languages: `export ORIGINAL_CWD=$(pwd) && cd ${CLAUDE_SKILL_DIR} && uv run python transcript.py "$0" --list-languages`

## After downloading

1. Tell the user the file path where the transcript was saved
2. If the user asks you to read or summarize the transcript, use the Read tool to read the saved file
