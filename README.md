# creat

The previous scaffold-based project creation system has been removed.

The repository now keeps only:

- the core CLI shell
- the config loading and validation layer
- the command-module skeleton under `creat/cmd/`

The next implementation target is an AI-agent-supported project creation system.

## Requirements

- Python 3.11+
- uv

## Current CLI Surface

Available now:

- `creat config show`
- `creat config init`

Configuration resolution order:

- `creat --config path/to/creat.json ...` or `creat --config path/to/creat.toml ...`
- the user config at `~/.config/creat/creat.json` when it exists
- model defaults, with the selected path kept as the active write target

Commands and library code can read the active config through `creat.configs.get_config()` after startup initialization.

Removed:

- scaffold discovery
- project scaffolding commands
- sample regeneration workflow

## Development

Set up the local environment:

```shell
make local
```

If you already activated `.venv`, `make local` will sync that active environment so the `creat` console script is available on your shell `PATH`.

Run the CLI:

```shell
uv run creat --help
```

Run checks:

```shell
make check
```
