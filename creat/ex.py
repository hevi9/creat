""" mk related exceptions. """

from creat.discovers import Location


class Error(Exception):
    """Base exception for mk excpetions."""


class DuplicateSourceError(Error):
    """Duplicate source id exists."""

    location: Location
    id2: str

    def __init__(self, msg, id2: str, location: Location):
        super().__init__(f"Duplicate {id2} in {location}: {msg}")
        self.location = location
        self.id2 = id2


class FieldError(Error):
    """Error on item field definition."""

    location: Location
    field: str

    def __init__(self, msg, field: str, location: Location):
        super().__init__(f"Error in field {field} in {location}: {msg}")
        self.location = location
        self.field = field


class ValidateError(Error):
    """Error on validation."""
