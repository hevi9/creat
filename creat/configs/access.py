from threading import Lock
from typing import Generic

from . import ConfigNotInitializedError, ConfigT


class ConfigSlot(Generic[ConfigT]):
    """Typed handle for a process-global config snapshot.

    A library-level global accessor cannot infer ``ConfigT`` from a
    zero-argument function.  This slot carries the type information so
    callers can recover a typed config value through a generic helper
    function.
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._config: ConfigT | None = None
        self._config_sources: list[str] = []
        self._freezed = False

    @property
    def config_sources(self) -> tuple[str, ...]:
        """Ordered list of config sources that have been loaded into this
        slot.
        """
        return tuple(self._config_sources)

    def set(
        self,
        config: ConfigT,
        config_source: str | None = None,
        freeze: bool = False,
    ) -> ConfigT:
        if config is None:
            raise ValueError("config must not be None")
        if self._freezed:
            raise RuntimeError("config is freezed and cannot be modified")
        with self._lock:
            self._config = config
            if config_source is not None:
                self._config_sources.append(config_source)
            if freeze:
                self._freezed = True
            return config

    def get(self) -> ConfigT:
        config = self._config
        if config is None:
            raise ConfigNotInitializedError(
                "config has not been initialized; "
                "call init_config() at program startup"
            )
        return config

    def is_initialized(self) -> bool:
        return self._config is not None

    def reset(self) -> None:
        with self._lock:
            self._config = None
            self._config_sources.clear()
            self._freezed = False
