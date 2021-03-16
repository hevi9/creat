""" mk package common functions. """


def version() -> str:
    """ Get package version. """
    # pylint: disable=import-outside-toplevel
    try:
        import importlib.metadata

        return importlib.metadata.version(__package__)
    except ImportError as ex:
        return f"NO VERSION: {ex}"
