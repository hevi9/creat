""" mk package common functions. """
import logging
import sys
from colorsys import hls_to_rgb
from enum import Enum
from typing import Optional

from loguru import logger
from rich.console import Console
from rich.theme import Theme as RichTheme


def version() -> str:
    """ Get package version. """
    # pylint: disable=import-outside-toplevel
    try:
        import importlib.metadata

        return importlib.metadata.version(__package__)
    except ImportError as ex:
        return f"NO VERSION: {ex}"


def hsl(hue: float = 0.0, saturation: float = 1.0, light: float = 1.0) -> str:
    """Make rgb() string from HSL definition.

    :param hue: Capped to 0.0 - 360.0 .
    :param saturation: Capped to 0.0 - 1.0 .
    :param light: Capped to 0.0 - 1.0 .
    :return: rgb() formatted string.
    """
    r, g, b = hls_to_rgb(
        (hue % 360.0) / 360.0,
        max(min(light, 1.0), 0.0),
        max(min(saturation, 1.0), 0.0),
    )
    return "rgb({},{},{})".format(int(r * 255), int(g * 255), int(b * 255))


class Theme(Enum):
    """ Rich theme options. """

    INFO = "info"
    """ Theme for informatic information. """

    WARNING = "warning"
    """ Theme for warning information. """

    ERROR = "error"
    """ Theme for error information. """


def get_theme() -> RichTheme:
    """ Get rich theme. """
    light = 0.5
    saturation = 0.4
    return RichTheme(
        {
            Theme.INFO.value: "{}".format(hsl(180.0, saturation, light)),
            Theme.WARNING.value: "{}".format(hsl(30.0, saturation, light)),
            Theme.ERROR.value: "{}".format(hsl(0.0, saturation, light)),
        }
    )


_console: Optional[Console] = None


def get_console() -> Console:
    """ Get rich console. """
    global _console
    if not _console:
        _console = Console(theme=get_theme())
    return _console


class _InterceptHandler(logging.Handler):
    """Intercept std library logging events and redirect them to loguru.

    See:
    https://loguru.readthedocs.io/en/stable/overview.html?highlight=logging#entirely-compatible-with-standard-logging
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger(level: str = "INFO"):
    """ Setup logger. """

    logger.remove()  # remove all loggers
    logger.add(
        sys.stderr,
        format="{file.path}:{line} <level>{message}</level>",
        level=level,
    )
    # noinspection PyArgumentList
    logging.basicConfig(handlers=[_InterceptHandler()], level=0)
