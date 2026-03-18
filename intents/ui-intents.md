TODO refine ui cli intents

### CLI contract

Keep the current entrypoint and commands stable during removal work:

- entry script in [pyproject.toml](../pyproject.toml)
- `creat list`
- `creat config user`
- `creat config scaffold [PATH] [--init]`
- `creat project <scaffold> <target> [--dry-run]`
- `creat sample <scaffold> [--sample-path PATH]`

### Config contract

- user config file remains JSON-based
- scaffold-local config file name remains `.creat.json` by default
- `UserConfig` fields remain compatible with current defaults
- `ScaffoldConfig.sample.runs[].text` remains the shell-run contract
