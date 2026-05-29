# chatbot/session.py

# Import UUID to create unique session identifiers
import uuid

# Import hostname and timestamps for basic session information
import socket
from datetime import datetime

# Import the audit logger
from chatbot.logging_utils import get_audit_logger


def start_session():
    """
    Creates a new session ID and logs the start of a chatbot session.

    This keeps session management separate from logging setup,
    so we can expand session handling later.
    """
    session_id = str(uuid.uuid4())
    start_time = datetime.now()
    hostname = socket.gethostname()

    audit_logger = get_audit_logger()
    audit_logger.info(
        f"SESSION START - ID={session_id} - Host={hostname} - Started at {start_time}"
    )

    return session_id, start_time


def end_session(session_id, start_time, reason="normal"):
    """
    Logs the end of a chatbot session.

    The reason might be:
    - normal
    - timeout
    - error
    """
    end_time = datetime.now()
    duration_seconds = (end_time - start_time).total_seconds()

    audit_logger = get_audit_logger()
    audit_logger.info(
        f"SESSION END - ID={session_id} - Ended at {end_time} - "
        f"Duration={duration_seconds:.1f}s - Exit={reason}"
    )
