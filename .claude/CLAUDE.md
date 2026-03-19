# Claude Skills Marketplace

A personal collection of Claude Code plugins distributed as a plugin marketplace.

## Project Structure

```
.claude-plugin/
  marketplace.json          # Registry of all plugins
plugins/<plugin-name>/
  .claude-plugin/
    plugin.json             # Plugin metadata (name, version, description, author)
  skills/<skill-name>/
    SKILL.md                # Skill definition (frontmatter + usage instructions)
    *.py                    # Python script(s) for the skill
    pyproject.toml          # Python dependencies (managed by uv)
    .python-version         # Python version pin
```

## Conventions

- **Package manager**: All Python skills use [uv](https://docs.astral.sh/uv/) — never pip directly.
- **ORIGINAL_CWD pattern**: Skills run via `cd ${CLAUDE_SKILL_DIR}`, so scripts use `os.environ.get("ORIGINAL_CWD", os.getcwd())` to resolve output paths relative to the caller's directory.
- **stderr / stdout**: Progress and status messages go to stderr. The final output path (or primary result) goes to stdout so the skill runner can capture it.
- **SKILL.md frontmatter**: Must include `name`, `description`, `argument-hint`, and `allowed-tools`.
- **Quality**: Keep scripts self-contained with minimal dependencies.

## Adding a New Skill

1. Create `plugins/<name>/.claude-plugin/plugin.json`
2. Create `plugins/<name>/skills/<name>/` with `SKILL.md`, script, `pyproject.toml`, `.python-version`
3. Run `uv sync` inside the skill directory to generate `uv.lock`
4. Add the plugin entry to `.claude-plugin/marketplace.json`
5. Update `README.md` with the new plugin row
