"""
Structured Logging - HERPath AI
=================================

Centralized logging configuration with structured output,
log levels, and format consistency.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler

from config.constants import LoggingConfig

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Global logger registry
_loggers = {}


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get or create a structured logger.
    
    Args:
        name: Logger name (usually __name__)
        level: Log level override (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    if name in _loggers:
        return _loggers[name]
    
    logger = logging.getLogger(name)
    
    # Set level
    log_level = level or LoggingConfig.DEFAULT_LEVEL
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Console handler (INFO and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LoggingConfig.CONSOLE_LEVEL))
    console_formatter = logging.Formatter(
        LoggingConfig.LOG_FORMAT,
        datefmt=LoggingConfig.DATE_FORMAT
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (DEBUG and above) with rotation
    log_file = LOGS_DIR / LoggingConfig.LOG_FILE
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=LoggingConfig.MAX_LOG_SIZE_MB * 1024 * 1024,
        backupCount=LoggingConfig.BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(getattr(logging, LoggingConfig.FILE_LEVEL))
    file_formatter = logging.Formatter(
        LoggingConfig.LOG_FORMAT,
        datefmt=LoggingConfig.DATE_FORMAT
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Cache logger
    _loggers[name] = logger
    
    return logger


def log_api_call(
    logger: logging.Logger,
    provider: str,
    endpoint: str,
    status_code: Optional[int] = None,
    duration_ms: Optional[float] = None,
    error: Optional[str] = None
) -> None:
    """
    Log API call with structured format.
    
    Args:
        logger: Logger instance
        provider: API provider name (e.g., "Gemini")
        endpoint: API endpoint called
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
        error: Error message if failed
    """
    if error:
        logger.error(
            f"API_CALL_FAILED | Provider={provider} | Endpoint={endpoint} | "
            f"Error={error}"
        )
    else:
        logger.info(
            f"API_CALL_SUCCESS | Provider={provider} | Endpoint={endpoint} | "
            f"Status={status_code} | Duration={duration_ms:.2f}ms"
        )


def log_agent_execution(
    logger: logging.Logger,
    agent_name: str,
    action: str,
    status: str,
    details: Optional[str] = None
) -> None:
    """
    Log agent execution events.
    
    Args:
        logger: Logger instance
        agent_name: Name of the agent
        action: Action performed (START, EXECUTE, COMPLETE, FAIL)
        status: Execution status
        details: Additional details
    """
    level = logging.INFO if status == "SUCCESS" else logging.WARNING
    
    log_msg = f"AGENT_{action} | Agent={agent_name} | Status={status}"
    if details:
        log_msg += f" | Details={details}"
    
    logger.log(level, log_msg)


def log_user_action(
    logger: logging.Logger,
    user_id: str,
    action: str,
    page: Optional[str] = None,
    details: Optional[str] = None
) -> None:
    """
    Log user actions for analytics.
    
    Args:
        logger: Logger instance
        user_id: User identifier (hashed for privacy)
        action: Action taken
        page: Page/view where action occurred
        details: Additional context
    """
    log_msg = f"USER_ACTION | UserID={user_id[:8]}... | Action={action}"
    if page:
        log_msg += f" | Page={page}"
    if details:
        log_msg += f" | Details={details}"
    
    logger.info(log_msg)


# Create default application logger
app_logger = get_logger("herpath_ai")
