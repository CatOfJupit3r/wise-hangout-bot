import os
from dotenv import load_dotenv
import logging
from logging.config import dictConfig


load_dotenv()


# CONSTANTS

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

# CONFIGS

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s - %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s - %(message)s"
        },
    },
    'handlers': {
        "console": {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file_general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/general.log',
            'mode': 'a',
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'mode': 'a',
            'formatter': 'verbose',
            'encoding': 'utf-8'
        }
    },
    "loggers": {
        "general": {
            "handlers": ["file_general"],
            "level": "INFO",
            "propagate": False
        },
        "errors": {
            "handlers": ["file_errors", "console"],
            "level": "ERROR",
            "propagate": False
        }
    }
}

# CONFIGURE LOGGING

dictConfig(LOGGING_CONFIG)

# CREATE LOGGERS

logger_errors = logging.getLogger("errors")
logger_general = logging.getLogger("general")

# FUNCTIONS


def generate_id() -> str:
    """
    Generates random id
    :return: str
    """
    import uuid
    return str(uuid.uuid4())
