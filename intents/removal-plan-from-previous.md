# Staged Removal Plan From Previous Codebase

## Goal

Prepare a safe decommission path for verified legacy parts of the current codebase without executing removals in this phase.

This document is intentionally limited to preparation. No runtime code changes are executed here.

## Scope Of "Old Codebase" For The First Removal Pass

The strongest verified removal candidates are the duplicate global-config accessors in [creat/configs.py](../creat/configs.py) and the redundant initialization call in [creat/**main**.py](../creat/__main__.py).

These candidates are safer than broader redesign targets because they are either unused or clearly duplicated by the active `ConfigAccess` path.

## Verified Decommission Candidates

| Candidate                                              | Current status                                  | Evidence                                                                                                     | Proposed action                           |
| ------------------------------------------------------ | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| `init_user_config`                                     | Redundant                                       | [creat/**main**.py](../creat/__main__.py) initializes `x_user_config` and then also calls `init_user_config` | Remove after behavior-preservation checks |
| `user_config`                                          | Unused accessor                                 | Defined in [creat/configs.py](../creat/configs.py); no call sites in `creat/`                                | Remove                                    |
| `init_scaffold_config`                                 | Unused initializer                              | Defined in [creat/configs.py](../creat/configs.py); no call sites in `creat/`                                | Remove                                    |
| `scaffold_config`                                      | Unused accessor                                 | Defined in [creat/configs.py](../creat/configs.py); no call sites in `creat/`                                | Remove                                    |
| `x_scaffold_config`                                    | Unused `ConfigAccess` instance                  | Defined in [creat/configs.py](../creat/configs.py); no call sites in `creat/`                                | Remove                                    |
| `__user_config` and `__scaffold_config` module globals | Dead state after removal of duplicate accessors | Defined in [creat/configs.py](../creat/configs.py)                                                           | Remove together with duplicate accessors  |

## Not In Scope For This First Pass

- [tests/test_idsubs.py](../tests/test_idsubs.py): `IdSubs` appears only in tests. It is not part of the current packaged runtime, so it should not be treated as removal work unless the product direction later changes.
- [creat/scaffolds.py](../creat/scaffolds.py): scaffold discovery is central to the current CLI and should be preserved until a replacement exists.
- [creat/cmd/project.py](../creat/cmd/project.py) and [creat/cmd/sample.py](../creat/cmd/sample.py): these commands are core product behavior and should be redesigned only behind stable command interfaces.

## Interfaces That Must Be Preserved

### CLI contract

Keep the current entrypoint and commands stable during removal work:

- entry script in [pyproject.toml](../pyproject.toml)
- `creat list`
- `creat config user`
- `creat config scaffold [PATH] [--init]`
- `creat project <scaffold> <target> [--dry-run]`
- `creat sample <scaffold> [--sample-path PATH]`

### Config contract

Preserve these current facts unless a migration is explicitly approved:

- user config file remains JSON-based
- scaffold-local config file name remains `.creat.json` by default
- `UserConfig` fields remain compatible with current defaults
- `ScaffoldConfig.sample.runs[].text` remains the shell-run contract

### Behavioral contract

Preserve the current rendering path through Copier and the current sample workflow semantics, including:

- initial sample render
- recopy on changes
- optional shell runs from scaffold config
- first-run Git initialization in the sample target

## Staged Execution Plan

### Stage 0. Freeze behavior with targeted tests

Before removing code, add coverage around the current public CLI behavior and config loading path.

Minimum useful coverage:

- config bootstrap with missing user config file
- scaffold discovery from configured roots
- `project` command calling Copier with expected arguments
- `sample` command first-run and recopy behavior

Reason:

The repository currently lacks CLI integration tests, so even safe-looking cleanup should be guarded.

### Stage 1. Remove the redundant init path

Target:

- remove the `init_user_config` import and call from [creat/**main**.py](../creat/__main__.py)

Reason:

- `x_user_config.init(config_data)` already initializes the active config path used elsewhere.

Expected outcome:

- no CLI behavior change
- one fewer state path to maintain

### Stage 2. Remove duplicate global config accessors

Target:

- delete `init_user_config`, `user_config`, `init_scaffold_config`, `scaffold_config`, `__user_config`, `__scaffold_config`, and `x_scaffold_config` from [creat/configs.py](../creat/configs.py)

Reason:

- they are unused or redundant relative to the active `ConfigAccess` path

Expected outcome:

- smaller config surface
- less ambiguity about the supported access pattern

### Stage 3. Clean follow-on references and docs

Target:

- update internal docs and comments to point only to `x_user_config`
- remove stale references from any future tests or examples

Reason:

- removal is incomplete if internal documentation keeps advertising deleted paths

### Stage 4. Reassess broader redesign targets

After the first-pass cleanup is complete, reassess larger changes such as:

- separating config validation concerns from config models
- isolating Copier behind an internal adapter
- breaking `sample` into smaller units with narrower side effects

These are redesign candidates, not immediate removal tasks.

## Risks And Unknowns

- The repository does not currently define a formal public Python API boundary beyond the CLI, so external imports of config helpers cannot be fully ruled out.
- The README is sparse, so behavior expectations come mostly from code rather than documentation.
- Because there are no CLI integration tests yet, accidental behavior regressions are the main risk during cleanup.

## Exit Criteria For Starting Actual Removal

Removal execution can begin once these conditions are met:

- source-backed tests exist for the current CLI behavior being preserved
- symbol search still confirms no internal call sites for the duplicate config helpers
- the work is explicitly approved as a code-removal change rather than a research or planning step

## Current Status

Prepared only.

No removal has been executed in this phase.
