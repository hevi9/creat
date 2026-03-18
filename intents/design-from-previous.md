# Design From Previous Codebase

## Summary

`creat` is a small Python CLI application packaged with Poetry. Runtime behavior is organized around Typer commands that load Pydantic configuration, discover scaffold directories from local roots, and use Copier to render templates. The `sample` command extends the main rendering path with file watching, recopy, and optional shell execution.

## Repository Structure

- [creat/**main**.py](../creat/__main__.py): root Typer app, subcommand wiring, user config bootstrap
- [creat/configs.py](../creat/configs.py): config models, config access helpers, JSON validation, error location mapping
- [creat/scaffolds.py](../creat/scaffolds.py): `Scaffold` abstraction and scaffold discovery
- [creat/processes.py](../creat/processes.py): `cd` context manager used by sample execution
- [creat/cmd/config.py](../creat/cmd/config.py): config inspection and local config initialization
- [creat/cmd/ls.py](../creat/cmd/ls.py): list available scaffolds
- [creat/cmd/project.py](../creat/cmd/project.py): instantiate a target project from a scaffold
- [creat/cmd/sample.py](../creat/cmd/sample.py): watch scaffold changes and regenerate a sample target
- [tests/test_idsubs.py](../tests/test_idsubs.py): isolated unit tests for a test-local substitution helper

## Runtime Flow

1. The root CLI callback in [creat/**main**.py](../creat/__main__.py) loads the user config JSON or falls back to defaults.
2. Commands that need scaffold lookup call `build_index()` from [creat/scaffolds.py](../creat/scaffolds.py).
3. Each `Scaffold` instance reads a local scaffold config file named by `UserConfig.scaffold_config_name`, defaulting to `.creat.json`.
4. Project rendering uses `copier.Worker` from [creat/cmd/project.py](../creat/cmd/project.py).
5. Sample rendering in [creat/cmd/sample.py](../creat/cmd/sample.py) uses `run_copy()` on first render, `run_recopy()` on updates, and optional shell commands from scaffold config.
6. The sample command then watches the scaffold directory with `watchfiles.watch()` and repeats the update cycle.

## Module Responsibilities

### CLI assembly

- The Typer application is built in [creat/**main**.py](../creat/__main__.py).
- Subcommands are contributed from the `creat/cmd` package.
- The package entry script is defined in [pyproject.toml](../pyproject.toml) as `creat = 'creat.__main__:cli'`.

### Configuration layer

- `UserConfig` defines the user config file path, scaffold config file name, and scaffold root directories.
- `ScaffoldConfig` defines scaffold-local behavior, currently centered on `sample.runs` shell commands.
- `json_to_obj()` validates JSON by calling `Model.model_validate_json()` and enriches validation failures with line and column data using `json-source-map`.
- `ConfigAccess[T]` provides the active runtime access path for config through `x_user_config`.

### Scaffold abstraction

- `Scaffold` wraps a scaffold root path and its resolved local config.
- `build_index()` performs filesystem discovery across all configured scaffold roots and returns a dictionary keyed by scaffold directory name.

### Process and shell handling

- `cd` in [creat/processes.py](../creat/processes.py) is a context manager that switches directories and prints Rich rules when entering and leaving.
- The sample command uses `subprocess.run(..., shell=True, check=True)` for configured shell commands.

## Development Stack

### Runtime dependencies

- Python: `>=3.11,<4` in [pyproject.toml](../pyproject.toml)
- CLI: `typer`
- Template rendering: `copier`, `jinja2`
- Data and validation: `pydantic`, `json-source-map`
- Output and logging: `rich`, `loguru`
- File watching: `watchfiles`
- Text and binary detection: `charset-normalizer`

### Packaging and environment

- Poetry is used for packaging and environment management.
- [poetry.toml](../poetry.toml) configures in-project virtual environments.
- [Makefile](../Makefile) provides local workflow targets such as `local`, `check`, `lock`, `update`, and `deploy-user`.

### Quality and CI

- Formatting: `black`
- Linting: `ruff`
- Type checking: `mypy` with the Pydantic plugin
- Testing: `pytest` with benchmark, coverage, mock, and timeout plugins
- Hooks: `pre-commit`
- CI: GitHub Actions in [.github/workflows/pr-main.yml](../.github/workflows/pr-main.yml) for Python 3.12 and 3.13

## Verified Design Facts

- The codebase is intentionally small and file-oriented; there is no service boundary or persistence layer beyond JSON config files.
- Configuration is JSON-only in the current implementation.
- Scaffold lookup is uncached and re-scans configured roots each time `build_index()` is called.
- The sample workflow has side effects beyond rendering: on first render it initializes a Git repository and makes an initial commit in the sample target.
- Error reporting for invalid config files is more advanced than the rest of the UX because it includes source locations.

## Notable Gaps And Inconsistencies

- [README.md](../README.md) says installation requires Python 3.12+, while [pyproject.toml](../pyproject.toml) allows Python 3.11+.
- Package metadata still contains placeholder author information in [pyproject.toml](../pyproject.toml).
- There are no CLI integration tests; current automated tests cover only [tests/test_idsubs.py](../tests/test_idsubs.py).
- `tests/test_idsubs.py` contains a helper that appears potentially reusable, but it is not part of the packaged runtime.
- The config layer contains both an active config-access pattern and a duplicate legacy-style global config path, which creates avoidable complexity.

## Design Implications For A Major Change

- The safest seam for replacement is the internals behind command execution, not the CLI contract itself.
- Config loading and scaffold discovery are central and should be preserved or migrated behind compatible interfaces.
- The sample command needs special handling during any redesign because it mixes rendering, Git side effects, shell execution, and file watching in one place.
