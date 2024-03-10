from pathlib import Path

from .configs import x_user_config, json_to_obj, ScaffoldConfig


class Scaffold:
    _root: Path
    _config: ScaffoldConfig

    def __init__(self, root: Path) -> None:
        self._root = root
        try:
            config_data = json_to_obj(
                self._root / x_user_config().scaffold_config_name,
                ScaffoldConfig,
            )
        except FileNotFoundError:
            config_data = ScaffoldConfig()
        self._config = config_data

    @property
    def root(self) -> Path:
        return self._root

    @property
    def id(self) -> str:
        return self.root.name

    @property
    def config(self) -> ScaffoldConfig:
        return self._config


def build_index() -> dict[str, Scaffold]:
    scaffolds = {}
    scaffolds_roots = [r.expanduser() for r in x_user_config().scaffolds_roots]
    for roots in scaffolds_roots:
        if roots.is_dir():
            for root in roots.iterdir():
                scaffold = Scaffold(root)
                scaffolds[scaffold.id] = scaffold
    return scaffolds
