from .config import Config


class DevConfig(Config):
    DEBUG = True
    ACCESS_LOG = True
    WORKERS = 1

    # 日志配置
    BASE_LOGGING = {
        'version': 1,
        'loggers': {
            "sanic.root": {"level": "DEBUG", "handlers": ["console", "console_err"], 'propagate': True},
            "sanic.error": {"level": "ERROR", "handlers": ["console_err"]},
        },
        'formatters': {
            'default': {
                'format': '%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
            },
            'console_err': {
                'class': 'logging.StreamHandler',
                'level': 'ERROR',
                'formatter': 'default',
            }
        }
    }
