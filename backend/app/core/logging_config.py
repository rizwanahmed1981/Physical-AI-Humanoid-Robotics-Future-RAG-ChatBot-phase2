import logging
import sys
import json
from datetime import datetime
from typing import Dict, Any

class StructuredFormatter(logging.Formatter):
    """
    Custom structured formatter for JSON logging
    """
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Add any extra fields passed to the log record
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'lineno', 'funcName', 'created',
                          'msecs', 'relativeCreated', 'thread', 'threadName',
                          'processName', 'process', 'getMessage', 'exc_info',
                          'exc_text', 'stack_info']:
                log_entry[key] = value

        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_entry)

def setup_logging():
    """
    Set up structured logging for the application
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create structured formatter
    structured_formatter = StructuredFormatter()

    # Add formatter to handler
    console_handler.setFormatter(structured_formatter)

    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

# Initialize logging
app_logger = setup_logging()

def get_logger(name: str = None):
    """
    Get a logger instance with the specified name
    """
    if name:
        return logging.getLogger(name)
    return app_logger