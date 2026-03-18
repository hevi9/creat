# creat

The previous scaffold-based project creation system has been removed.

The repository now keeps only:

- the core CLI shell
- the JSON config loading and validation layer
- the command-module skeleton under `creat/cmd/`

The next implementation target is an AI-agent-supported project creation system.

## Requirements

- Python 3.11+
- uv

## Current CLI Surface

Available now:

- `creat config user`
- `creat config init`

Removed:

- scaffold discovery
- project scaffolding commands
- sample regeneration workflow

## Development

Set up the local environment:

```shell
make local
```

Run the CLI:

```shell
uv run creat --help
```

Run checks:

```shell
make check
```
