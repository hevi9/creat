# Scope

These instructions apply to the entire repository.

# Project

- This repository is the CLI and config foundation for an AI-agent-supported project creation system.
- The previous scaffold-based implementation has been removed.
- Keep the `creat/cmd/` package structure in place for future commands.
- Preserve and extend the config system in `creat/configs.py` unless a broader redesign is requested.
- `intents/` is development file tree for project intents that are to be redefined and implemented to code by agents.
    - do not modify `intents/**` unless you are working with intents phase

# Stack

- Python 3.11+
- `uv` for environment and task execution
- `typer` for the CLI
- `pydantic` for config models and validation
- `loguru` for logging
    - reference: https://loguru.readthedocs.io/en/stable/

# Working Rules

- Prefer minimal, focused changes.
- Do not reintroduce scaffold-specific code or dependencies unless explicitly requested.
- Update tests and documentation when changing behavior.
- On not clear choices ask user for reference.

# Useful Commands

- `make local`
- `make check`
- `uv run creat --help`

# Support developer review

- Add reason code comments, that give purpose for code.
- Respect code change markers: TODO, FIXME
