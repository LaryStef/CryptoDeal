# import multiprocessing
import os


log_directory: str = os.path.dirname("logs/")
os.makedirs(log_directory, exist_ok=True)


bind = "127.0.0.1:8000"
worker_class = "sync"
# workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "main:app"
reload = True
backlog = 1024
timeout = 360
capture_output = True
logconfig_dict = dict(
    version=1,
    disable_existing_loggers=False,
    root={"level": "INFO", "handlers": [
        "general_file",
        "error_file",
        "error_console"
    ]},
    loggers={
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["error_console", "error_file"],
            "propagate": True,
            "qualname": "gunicorn.error"
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["general_file", "error_file", "error_console"],
            "propagate": True,
            "qualname": "gunicorn.access"
        }
    },
    handlers={
        "error_console": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "generic",
            "stream": "ext://sys.stderr"
        },
        'general_file': {
            'level': 'INFO',
            'formatter': 'generic',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/app.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'error_file': {
            'level': 'ERROR',
            'formatter': 'generic',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/errors.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
    },
    formatters={
        "generic": {
            "format": "[%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        }
    }
)
