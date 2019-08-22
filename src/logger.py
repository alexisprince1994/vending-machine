import logging
import logging.handlers
import sys

# Gotta make it pretty
import colorama

colorama_stdout = sys.stdout
colorama_wrap = True

colorama.init(wrap=colorama_wrap)


DEBUG = logging.DEBUG
NOTICE = 15
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

logging.addLevelName(NOTICE, "NOTICE")


class Logger(logging.Logger):
    """
    Subclassing the builtin logger to make our new NOTICE level work.
    """

    def notice(self, msg, *args, **kwargs):
        if self.isEnabledFor(NOTICE):
            self._log(NOTICE, msg, args, **kwargs)


logging.setLoggerClass(Logger)

if sys.platform == "win32" and not os.environ.get("TERM"):
    colorama_wrap = False
    colorama_stdout = colorama.AnsiToWin32(sys.stdout).stream

elif sys.platform == "win32":
    colorama_wrap = False

stdout_handler = logging.StreamHandler(colorama_stdout)
stdout_handler.setFormatter(logging.Formatter("%(message)s"))
stdout_handler.setLevel(NOTICE)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(logging.Formatter("%(message)s"))
stderr_handler.setLevel(WARNING)


logger = logging.getLogger("vending-machine")
logger.addHandler(stdout_handler)
logger.setLevel(DEBUG)
logging.getLogger().setLevel(CRITICAL)

# Redirect warnings through our logging setup
# They will be logged to a file below
logging.captureWarnings(True)


initialized = False


def _swap_handler(logger, old, new):
    if old in logger.handlers:
        logger.handlers.remove(old)
    if new not in logger.handlers:
        logger.addHandler(new)


def log_to_stderr(logger):
    _swap_handler(logger, stdout_handler, stderr_handler)


def log_to_stdout(logger):
    _swap_handler(logger, stderr_handler, stdout_handler)


class ColorFilter(logging.Filter):
    def filter(self, record):

        msg = record.msg

        for escape_sequence in src.ui.COLORS.values():
            subbed = msg.replace(escape_sequence, "")
        record.msg = subbed

        return True


def default_formatter():
    return logging.Formatter("%(asctime)-18s: %(message)s")


# def initialize_logger(debug_mode=False, path=None):
#     global initialized, logger, stdout_handler, stderr_handler

#     if initialized:
#         return

#     if debug_mode:
#         # we'll only use one of these, but just set both up
#         stdout_handler.setFormatter(default_formatter())
#         stdout_handler.setLevel(DEBUG)
#         stderr_handler.setFormatter(default_formatter())
#         stderr_handler.setLevel(DEBUG)

#     if path is not None:
#         make_log_dir_if_missing(path)
#         log_path = os.path.join(path, 'vending-machine.log')

#         # log to directory as well
#         logdir_handler = logging.handlers.TimedRotatingFileHandler(
#             filename=log_path,
#             when='d',
#             interval=1,
#             backupCount=7,
#         )

#         color_filter = ColorFilter()
#         logdir_handler.addFilter(color_filter)

#         logdir_handler.setFormatter(default_formatter())
#         logdir_handler.setLevel(DEBUG)

#         logger.addHandler(logdir_handler)

#         # Log Python warnings to file
#         warning_logger = logging.getLogger('py.warnings')
#         warning_logger.addHandler(logdir_handler)
#         warning_logger.setLevel(DEBUG)

#     initialized = True


def logger_initialized():
    return initialized


def log_cache_events(flag):
    """Set the cache logger to propagate its messages based on the given flag.
    """
    CACHE_LOGGER.propagate = flag


GLOBAL_LOGGER = logger
