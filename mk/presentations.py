from typing import Union


def scalar_to_bool(scalar: Union[bool, str]) -> bool:
    """ Decode scalar to bool. """
    if isinstance(scalar, bool):
        return scalar
    if isinstance(scalar, str):
        value = str(scalar)
        if value in ("True", "true"):
            return True
        return False
    raise TypeError(f"{scalar} is not type of str or bool")
