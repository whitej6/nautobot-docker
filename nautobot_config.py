"""Nautobot configuration file."""
from distutils.util import strtobool
import os
import sys


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.
    Examples:
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg
    return bool(strtobool(str(arg)))

REQUIRED_ENV_VARS = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "REDIS_HOST",
    "REDIS_PORT",
    "SECRET_KEY"
]

for i in REQUIRED_ENV_VARS:
    if i not in os.environ:
        raise ValueError(f"Missing required environment variable {i}.")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(" ")

DATABASES = {
    "default": {
        "NAME": os.environ.get("DB_NAME", "nautobot"),
        "USER": os.environ.get("DB_USER", ""),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", ""),
        "CONN_MAX_AGE": 300,
        "ENGINE": "django.db.backends.postgresql",
    }
}

DEBUG = False

LOG_LEVEL = "INFO"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "normal": {
            "format": "%(asctime)s.%(msecs)03d %(levelname)-7s %(name)s :\n  %(message)s",
            "datefmt": "%H:%M:%S",
        },
        "verbose": {
            "format": "%(asctime)s.%(msecs)03d %(levelname)-7s %(name)-20s %(filename)-15s %(funcName)30s() :\n  %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        "normal_console": {
            "level": "INFO",
            "class": "rq.utils.ColorizingStreamHandler",
            "formatter": "normal",
        },
        "verbose_console": {
            "level": "DEBUG",
            "class": "rq.utils.ColorizingStreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["normal_console"], "level": "INFO"},
        "nautobot": {
            "handlers": ["normal_console"],
            "level": LOG_LEVEL,
        },
        "rq.worker": {
            "handlers": ["normal_console"],
            "level": LOG_LEVEL,
        },
    },
}


RQ_QUEUES = {
    "default": {
        "HOST": os.environ.get("REDIS_HOST"),
        "PORT": int(os.environ.get("REDIS_PORT", 6379)),
        "DB": 0,
        "PASSWORD": os.environ.get("REDIS_PASSWORD"),
        "SSL": is_truthy(os.environ.get("REDIS_SSL", False)),
        "DEFAULT_TIMEOUT": 300,
    },
    "check_releases": {
        "HOST": os.environ.get("REDIS_HOST"),
        "PORT": int(os.environ.get("REDIS_PORT", 6379)),
        "DB": 0,
        "PASSWORD": os.environ.get("REDIS_PASSWORD"),
        "SSL": is_truthy(os.environ.get("REDIS_SSL", False)),
        "DEFAULT_TIMEOUT": 300,
    },
}

# REDIS CACHEOPS
CACHEOPS_REDIS = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/2"


SECRET_KEY = os.environ.get("SECRET_KEY", "notverysecure")
