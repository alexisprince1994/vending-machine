from src.logger import GLOBAL_LOGGER as logger

# from src import logger
import src.ui.colors

import time

USE_COLORS = True
COLOR_FG_RED = src.ui.colors.COLORS["red"]
COLOR_FG_GREEN = src.ui.colors.COLORS["green"]
COLOR_FG_YELLOW = src.ui.colors.COLORS["yellow"]
COLOR_RESET_ALL = src.ui.colors.COLORS["reset_all"]

STATUSES = {"info": COLOR_FG_YELLOW, "success": COLOR_FG_GREEN, "error": COLOR_FG_RED}


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
    # logger.info("{} | {}: {}".format(get_timestamp(), fancy_status, message))


def formatted_print(message: str) -> None:
    """
    Responsible for the actual printing of the message
    with a timestamp. Doesn't enforce a status or coloring
    of the actual message
    """

    logger.info("{} | {}".format(get_timestamp(), message))


PRINTER_WIDTH = 80


def use_colors():
    global USE_COLORS
    USE_COLORS = True


def printer_width(printer_width):
    global PRINTER_WIDTH
    PRINTER_WIDTH = printer_width


def get_timestamp():
    return time.strftime("%H:%M:%S")


def color(text, color_code):
    if USE_COLORS:
        return "{}{}{}".format(color_code, text, COLOR_RESET_ALL)
    else:
        return text


def green(text):
    return color(text, COLOR_FG_GREEN)


def yellow(text):
    return color(text, COLOR_FG_YELLOW)


def red(text):
    return color(text, COLOR_FG_RED)


def print_timestamped_line(msg, use_color=None):
    if use_color is not None:
        msg = color(msg, use_color)

    logger.info("{} | {}".format(get_timestamp(), msg))


def print_fancy_output_line(msg, status, truncate=False):

    prefix = "{timestamp} | {message}".format(timestamp=get_timestamp(), message=msg)

    truncate_width = PRINTER_WIDTH - 3
    justified = prefix.ljust(PRINTER_WIDTH, ".")
    if truncate and len(justified) > truncate_width:
        justified = justified[:truncate_width] + "..."

    status_txt = status

    output = "{justified} [{status}]".format(justified=justified, status=status_txt)

    logger.info(output)


def get_printable_result(result, success, error):
    if result.error is not None:
        info = "ERROR {}".format(error)
        status = red(result.status)
    else:
        info = "OK {}".format(success)
        status = green(result.status)

    return info, status


def print_model_result_line(result, description, index, total):
    info, status = get_printable_result(result, "created", "creating")

    print_fancy_output_line(
        "{info} {description}".format(info=info, description=description),
        status,
        index,
        total,
        result.execution_time,
    )
