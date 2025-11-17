import sys
import re
import logging
from loguru import logger
from app.config.settings import Settings


class InterceptHandler(logging.Handler):
    """
    Redirect standard logging records into Loguru.
    """
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # depth can be adjusted depending on your stack structure
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

class RedactQueryFilter(logging.Filter):
    """
    A logging filter that replaces the query string (?...) with ?<redacted>
    before the log record is emitted.

    This is intended for uvicorn.access logging lines.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            if record.args and len(record.args) >= 3:
                # Typically the path with query string.
                path_qs = record.args[2] 
                # Redact query string.
                redacted = re.sub(r'\?.*', '?<redacted>', path_qs) 
                # Rebuild args with redacted path.
                args = list(record.args)
                args[2] = redacted
                record.args = tuple(args)
            return True
        except Exception:
            return True

def configure_logging(settings: Settings):
    """
    Configure Loguru logging based on environment variables provided by Settings.
    """

    # Load settings
    log_level = settings.LOG_LEVEL
    log_message_file = settings.LOG_MESSAGE_FILE
    log_error_file = settings.LOG_ERROR_FILE
    json_format = settings.LOG_JSON_FORMAT
    diagnose = settings.LOG_DIAGNOSE
    backtrace = settings.LOG_BACKTRACE

    # file_format = (
    #     "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
    #     "{name}:{function}:{line} | {message}"
    # )

    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message}"
    )

    # Remove default Loguru configuration
    logger.remove()

    # JSON log format = serialized output
    if json_format:
        colorize = False
        serialize = True
    else:
        colorize = False
        serialize = False

    # Sink 1: normal log file (info/debug/warning)
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

    # Sink 2: error log file (ERROR+)
    logger.add(
        sink=log_error_file,
        level="ERROR",
        format=file_format,
        rotation="5 MB",
        retention="7 days",
        compression="zip",
        serialize=serialize,
        colorize=colorize,
        diagnose=diagnose,
        backtrace=backtrace,
    )

    # Sink 3: console output
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | <level>{message}</level>",
        colorize=True,
        diagnose=diagnose,
        backtrace=backtrace,
    )

    # Redirect standard logging → Loguru
    logging.getLogger().handlers = []
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    # Configure specific modules
    modules = ["fastapi", "uvicorn", "uvicorn.error", "uvicorn.access"] # Modules to redirect to Loguru: "fastapi", "uvicorn", "uvicorn.error", etc.
    for name in modules:
        logger_std = logging.getLogger(name)
        logger_std.handlers = []
        logger_std.propagate = True  # Required for InterceptHandler to capture logs

    # --- NEW: Attach query-redaction filter to uvicorn.access ---
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.addFilter(RedactQueryFilter())
