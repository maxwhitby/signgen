"""
Logging configuration for Sign Generator
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class SignGeneratorLogger:
    """Custom logger with file and console output"""

    def __init__(self, name="SignGenerator", log_dir=None, debug=False):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        self.logger.handlers.clear()

        # Create log directory
        if log_dir is None:
            log_dir = Path.home() / ".sign_generator" / "logs"
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        # File handler for detailed logs
        log_file = log_dir / f"signgen_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)

        # Console handler for important messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO if not debug else logging.DEBUG)
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

    def set_debug(self, enabled):
        """Toggle debug mode"""
        level = logging.DEBUG if enabled else logging.INFO
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(level)


# Global logger instance
_logger_instance = None


def get_logger(debug=False):
    """Get or create the global logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SignGeneratorLogger(debug=debug)
    return _logger_instance.get_logger()


def set_debug_mode(enabled):
    """Enable or disable debug mode globally"""
    global _logger_instance
    if _logger_instance:
        _logger_instance.set_debug(enabled)