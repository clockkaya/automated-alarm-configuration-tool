import logging
import os
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored_formatter': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s',
            'datefmt': None,
            'reset': True,
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            'secondary_log_colors': {},
            'style': '%'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join('F:/pydir/selenium/logs', 'app.log'),
            'formatter': 'colored_formatter',
            'level': 'DEBUG',
        },
        'console': {
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored_formatter',
            'level': 'INFO',
        },
    },
    'loggers': {
        '': {  # 根记录器
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


def main():
    # 使用字典配置日志
    logging.config.dictConfig(LOGGING_CONFIG)