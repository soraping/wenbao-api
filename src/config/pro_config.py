import multiprocessing
import os
from datetime import date
from src.config.config import Config


class ProConfig(Config):
    DEBUG = False
    ACCESS_LOG = True
    # WORKERS = multiprocessing.cpu_count()

    # 日志文件路径
    LOGGING_INFO_FILE = os.path.join(Config.BASE_DIR, "..", f'logs/{date.today()}/info.log')
    LOGGING_ERROR_FILE = os.path.join(Config.BASE_DIR, "..", f'logs/{date.today()}/error.log')

    # 日志配置
    BASE_LOGGING = {
        'version': 1,
        'loggers': {
            "sanic.root": {
                "level": "INFO",
                "handlers": ['info_file', 'error_file'],
                'propagate': True
            },
            "sanic.error": {"level": "ERROR", "handlers": ["error_file"]},
        },
        'formatters': {
            'default': {
                'format': '%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s',
            }
        },
        'handlers': {
            'info_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_INFO_FILE,
                'maxBytes': (1 * 1024 * 1024),
                'backupCount': 10,
                'encoding': 'utf8',
                'level': 'INFO',
                'formatter': 'default',
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGGING_ERROR_FILE,
                'maxBytes': (1 * 1024 * 1024),
                'backupCount': 10,
                'encoding': 'utf8',
                'level': 'ERROR',
                'formatter': 'default',
            },
        }
    }


if __name__ == '__main__':
    print(ProConfig.get_config())
