import time


import vending_machine.ui.colors
from vending_machine.utils import GLOBAL_LOGGER as logger

USE_COLORS = True
COLOR_FG_RED = vending_machine.ui.colors.COLORS["red"]
COLOR_FG_GREEN = vending_machine.ui.colors.COLORS["green"]
COLOR_FG_YELLOW = vending_machine.ui.colors.COLORS["yellow"]
COLOR_RESET_ALL = vending_machine.ui.colors.COLORS["reset_all"]

STATUSES = {"info": COLOR_FG_YELLOW, "success": COLOR_FG_GREEN, "error": COLOR_FG_RED}


def get_timestamp():
    """
    Quick utility method to ensure consistently formatted timestamps
    are able to be logged to the user.
    :return:
    """
    return time.strftime("%H:%M:%S")


def color(text, color_code):
    """
    Colors a piece of text and returns to the default after
    """

    return "{}{}{}".format(color_code, text, COLOR_RESET_ALL)


def fancy_print(status: str, message: str) -> None:
    """
    Prints the message to stdout so the user
    can have an interactive experience with
    the vending machine in a consistent way.
    """
    if status not in STATUSES.keys():
        raise ValueError(
            "Unknown status, need one of {} and got {}".format(STATUSES.keys(), status)
        )

    fancy_status = color(status.upper(), STATUSES[status])
    msg = "{}: {}".format(fancy_status, message)
    formatted_print(msg)


def formatted_print(message: str) -> None:
    """
    Responsible for the actual printing of the message
    with a timestamp. Doesn't enforce a status or coloring
    of the actual message
    """

    logger.info("{} | {}".format(get_timestamp(), message))
