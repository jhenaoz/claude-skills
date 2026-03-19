# Claude Skills

A personal collection of [Claude Code](https://claude.com/claude-code) plugins, distributed as a plugin marketplace.

## Quick Start

```bash
# Add the marketplace
/plugin-marketplace add jhenaoz/claude-skills

# Install a plugin
/plugin install youtube-transcript@claude-skills
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [ffmpeg](https://ffmpeg.org/) (for video download merging)
- Python 3.14+

## Available Plugins

| Plugin | Description | Usage |
|--------|-------------|-------|
| `youtube-transcript` | Download YouTube video transcripts | `/youtube-transcript:youtube-transcript <url>` |
| `youtube-download` | Download YouTube videos as MP4 | `/youtube-download:youtube-download <url>` |

## Permissions

Some plugins run Python scripts via `uv`. You may need to approve `Bash(uv run:*)` when prompted, or add it to your project's allowed permissions.

## Adding a New Plugin

1. Create a directory under `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` with name, version, and description
3. Add `skills/<skill-name>/SKILL.md` with the skill definition
4. Add any scripts and `pyproject.toml` for dependencies
5. Register the plugin in `.claude-plugin/marketplace.json`

### Plugin template

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        ├── script.py
        └── pyproject.toml
```
