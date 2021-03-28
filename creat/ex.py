""" mk related exceptions. """

from creat.location import Location


class MkError(Exception):
    """ Base exception for mk excpetions. """


class MkDuplicateSourceError(MkError):
    """ Duplicate source id exists. """

    location: Location
    id2: str

    def __init__(self, msg, id2: str, location: Location):
        super().__init__(f"Duplicate {id2} in {location}: {msg}")
        self.location = location
        self.id2 = id2


class MkFieldError(MkError):
    """ Error on item field definition. """

    location: Location
    field: str

    def __init__(self, msg, field: str, location: Location):
        super().__init__(f"Error in field {field} in {location}: {msg}")
        self.location = location
        self.field = field


class MkValidateError(MkError):
    """ Error on validation. """
