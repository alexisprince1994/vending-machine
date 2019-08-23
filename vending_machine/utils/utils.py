import string
from typing import Tuple


def position_from_coordinates(column: int, row: int) -> Tuple[str, int]:
    """
    Converts from a row and column number to a position tuple.
    """

    letter = string.ascii_uppercase[column - 1]

    return letter, row


def coordinates_from_position(position: Tuple[str, int]) -> Tuple[int, int]:
    """
    Converts from a position Tuple to row and column coordinates
    """

    # We're going to assume that the vending machine will never
    # have more than 26 columns (A through Z). Otherwise
    # this code will break, and a refactor will be required.
    # If there's a vending machine this large, please take
    # a picture and let me know, because that'd be incredible!

    conversion = {
        letter: indx + 1 for indx, letter in enumerate(string.ascii_uppercase)
    }

    return conversion[position[0]], position[1]
