""" mk related exceptions. """

from creat.discovers import Location


class Error(Exception):
    """Base exception."""

    location: Location

    def __str__(self):
        return f"{self.location}: {super().__str__()}"

    def __init__(self, msg: str, location: Location):
        super().__init__(msg)
        self.location = location


class DuplicateSourceError(Error):
    """Duplicate source id exists."""

    source_id: str

    def __str__(self):
        return f"{self.location}: {self.source_id}: {super().__str__()}"

    def __init__(self, msg, location: Location, source_id: str):
        super().__init__(msg, location=location)
        self.source_id = source_id


class FieldError(Error):
    """Error on item field definition."""

    field: str

    def __str__(self):
        return f"{self.location}: {self.field}: {super().__str__()}"

    def __init__(self, msg, location: Location, field: str):
        super().__init__(msg, location=location)
        self.field = field


class ValidateError(Error):
    """Error on validation."""
