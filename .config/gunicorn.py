workers = 4  # (os.cpu_count() or 1) * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"

logconfig_dict = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "gunicorn.error": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
