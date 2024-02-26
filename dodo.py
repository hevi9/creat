from pathlib import Path

DOIT_CONFIG = {
    "action_string_formatting": "new",
    "verbosity": 2,
    "default_tasks": ["local"],
}

dist_root = Path("./dist")
creat_pkg = dist_root / "creat-0.0.0-py3-none-any.whl"


def task_local():
    """Prepare local environment."""
    return {
        "actions": [
            "poetry install",
            "pre-commit install",
        ],
    }


def task_check():
    """Check files."""
    return {
        "actions": [
            "pre-commit run -a",
            "mypy creat",
        ],
    }


def task_install():
    """Install creat to user software with pipx."""
    return {
        "task_dep": ["check"],
        "actions": [
            "poetry build --no-interaction",
            f"pipx install --force {creat_pkg!s}",
        ],
    }
