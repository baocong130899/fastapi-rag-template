import sys
import logging
from loguru import logger
from app.config.settings import Settings


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def configure_logging():
    """
    Loguru configuration is based on environment variables from settings.
    """
    settings = Settings()

    # Setup default values.
    log_level = settings.LOG_LEVEL
    log_message_file = settings.LOG_MESSAGE_FILE
    log_error_file = settings.LOG_ERROR_FILE
    json_format = settings.LOG_JSON_FORMAT
    diagnose = (
        settings.LOG_DIAGNOSE
    )  # Display the values of variables at each frame of the stack trace.
    backtrace = (
        settings.LOG_BACKTRACE
    )  # Record the sequence of function calls leading to the point where the error occurred (traceback).
    file_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}"

    logger.remove()

    # 1. Define the format based on the LOG_JSON_FORMAT environment variable.
    if json_format:
        colorize = False
        serialize = True
    else:
        # Easy-to-read format for files and console (without using serialize).
        colorize = False
        serialize = False

    # 2. Sink 1: Regular logging (MESSAGE_FILE).
    logger.add(
        sink=log_message_file,
        level=log_level,
        format=file_format,
        serialize=serialize,
        rotation="1 MB",
        retention="3 days",
        compression="zip",
        enqueue=True,
        colorize=colorize,
        filter=lambda rec: rec["level"].no < logger.level("ERROR").no,
    )

    # 2. Sink 2: Regular logging (ERROR_FILE).
    logger.add(
        sink=log_error_file,
        level="ERROR",  # Only record from ERROR and above
        format=file_format,
        rotation="5 MB",
        retention="7 days",
        compression="zip",
        serialize=serialize,
        colorize=colorize,
        diagnose=diagnose,
        backtrace=backtrace,
    )

    # 4. Sink 3: Console (always keep it for easy debugging).
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {name} - <level>{message}</level>",
        colorize=True,
        diagnose=diagnose,
        backtrace=backtrace,
    )

    # 5. Block logs from the standard logging module.
    logging.getLogger().handlers = []
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
