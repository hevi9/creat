# creat

The previous scaffold-based project creation system has been removed.

The repository now keeps only:

- the core CLI shells (`creat` and `creatctl`)
- the config loading and validation layer
- the command-module skeleton under `creat/cmd/`

The next implementation target is an AI-agent-supported project creation system.

## Requirements

- Python 3.11+
- uv

## Current CLI Surface

### creat (project creation)

Currently a skeleton with `--version` support. Project creation commands will be added here.

### creatctl (operations/admin)

Available now:

- `creatctl config show`
- `creatctl config init`

Configuration resolution order:

- `creatctl --config path/to/creat.toml ...`
- the user config at `~/.config/creat/creat.toml` when it exists
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

If you already activated `.venv`, `make local` will sync that active environment so the `creat` and `creatctl` console scripts are available on your shell `PATH`.

Run the CLIs:

```shell
uv run creat --help
uv run creatctl --help
```

Run checks:

```shell
make check
```
