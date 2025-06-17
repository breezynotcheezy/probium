import json
import logging
import os
import sys
from logging.config import dictConfig


class JsonFormatter(logging.Formatter):
    """Pretty JSON formatter for console logs."""

    def format(self, record: logging.LogRecord) -> str:q
        obj = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.funcName:
            obj["func"] = record.funcName
        if record.exc_info:
            obj["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(obj, indent=2)


def setup_logging(level: str | int | None = None):
    level = level or os.getenv("FASTBACK_LOG", "WARNING")
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": "filter.logging_cfg.JsonFormatter",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "stream": sys.stdout,
                }
            },
            "root": {"handlers": ["console"], "level": level},
        }
    )
