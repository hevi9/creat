DOIT_CONFIG = {
    "action_string_formatting": "new",
    "verbosity": 2,
    "default_tasks": ["local"],
}


def task_local():
    """Prepare local environment."""
    return {
        "actions": [
            "poetry install",
            "pre-commit install"
        ],
    }


def task_check():
    """Check files."""
    return {
        "actions": [
            "pre-commit run -a"
        ],
    }
