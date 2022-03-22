from pathlib import Path

DOIT_CONFIG = {
    "action_string_formatting": "new",
    "verbosity": 2,
    "default_tasks": ["build"],
}

root = Path.cwd()


class prg:
    creat = "creat"


class files:
    models = list(root.rglob("./creat/models/**/*.py"))
    json_schema = Path("./json-schema/creat.json")


def task_schema():
    """Create json-schema for .create.yaml file validation."""
    return {
        "targets": [files.json_schema],
        "file_dep": files.models,
        "actions": [
            [prg.creat, "json-schema", files.json_schema],
        ],
    }


def task_build():
    """Build project"""
    return {
        "actions": None,
        "task_dep": ["schema"],
    }
