# chatbot/logging_utils.py

# Import logging tools
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Import log rotation settings
from chatbot.config import LOG_MAX_BYTES, LOG_BACKUP_COUNT


# Create log directories if they do not exist
BASE_LOG_DIR = Path("logs")
SYSTEM_LOG_DIR = BASE_LOG_DIR / "system_logs"
AUDIT_LOG_DIR = BASE_LOG_DIR / "audit"
CHAT_LOG_DIR = BASE_LOG_DIR / "chat_logs"

SYSTEM_LOG_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
CHAT_LOG_DIR.mkdir(parents=True, exist_ok=True)


def _create_rotating_logger(logger_name: str, log_file: Path, level: int, formatter: logging.Formatter):
    """
    Creates a rotating logger.

    The logger only gets a handler once.
    This prevents duplicate log lines if the function is called more than once.
    """
    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        logger.setLevel(level)

        handler = RotatingFileHandler(
            log_file,
            maxBytes=LOG_MAX_BYTES,      # 20 MB per file
            backupCount=LOG_BACKUP_COUNT # 5 files = approx 100 MB total
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Prevent logs from being duplicated by the root logger
        logger.propagate = False

    return logger


# === System Logger Setup ===
def get_system_logger():
    """
    Creates a system logger for technical errors and debug messages.

    This should be used for:
    - unexpected exceptions
    - Ollama/API failures
    - system-level issues
    - future file parsing issues
    """
    return _create_rotating_logger(
        logger_name="system_logger",
        log_file=SYSTEM_LOG_DIR / "system.log",
        level=logging.DEBUG,
        formatter=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"),
    )


# === Audit Logger Setup ===
def get_audit_logger():
    """
    Creates an audit logger for tracking user sessions.

    This should be used for:
    - session started
    - session ended
    - future user/session metadata
    """
    return _create_rotating_logger(
        logger_name="audit_logger",
        log_file=AUDIT_LOG_DIR / "audit.log",
        level=logging.INFO,
        formatter=logging.Formatter("%(asctime)s - %(message)s"),
    )


# === Chat Logger Setup ===
def get_chat_logger():
    """
    Creates a chat logger for tracking user sessions.

    Stores a history of all questions and responses.
    This could later be used for:
    - internal review
    - quality checks
    - model training consideration
    - internal training
    - external marketing examples

    Important:
    Chat logs can contain sensitive user data, so they should be handled carefully.
    """
    return _create_rotating_logger(
        logger_name="chat_logger",
        log_file=CHAT_LOG_DIR / "chat.log",
        level=logging.INFO,
        formatter=logging.Formatter("%(asctime)s - %(message)s"),
    )
