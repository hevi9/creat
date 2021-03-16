""" mk base objects. """

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Iterable, Mapping, Optional

from .ex import MkValidateError
from .location import Location
from .presentations import scalar_to_bool

if TYPE_CHECKING:
    from .index import Index


class Item(metaclass=ABCMeta):
    """ Base for structural control items. """

    _doc: Optional[str]
    _show: bool
    _location: Location

    def __init__(self, control: dict, location: Location):
        """ """
        self._doc = control.get("doc", None)
        self._show = scalar_to_bool(control.get("show", True))
        self._location = location

    @property
    def doc(self) -> Optional[str]:
        """ Documentation of the item. """
        return self._doc

    @property
    def show(self) -> bool:
        """ Show item on UI. """
        return self._show

    @property
    def location(self) -> Location:
        """ File location of the item. """
        return self._location

    def validate(self):
        """Validate item.

        :raises:  ValidateError on faulty item."""
        raise MkValidateError(f"Validation error on item in location {self._location}")


class Updateable(metaclass=ABCMeta):
    """ Update control items in pass 2. """

    @abstractmethod
    def update(self, index: Index) -> None:
        """ Update index on pass 2. """


class Runnable(Updateable):
    """ Runnable items. """

    @abstractmethod
    def run(self, context: Mapping[str, Any]) -> None:
        """ Run action, either direct or composite. """

    def programs(self) -> Iterable[str]:
        """ External programs used in this run context. """
        return
        # noinspection PyUnreachableCode
        # pylint: disable=unreachable
        yield  # NOSONAR

    @property
    @abstractmethod
    def cd(self) -> Optional[str]:
        """ Current working directory in this run context. """

    @property
    @abstractmethod
    def env(self) -> Mapping[str, str]:
        """ Environment variables in this run context. """
