import logging
import logging.config

from src.helpers.ids import request_id


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'DEBUG': BLUE,
    'INFO': WHITE,
    'WARNING': MAGENTA,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

BOLD_COLOR_SEQ = "\033[1;%dm"
COLOR_SEQ = "\033[%dm"
RESET_SEQ = "\033[0m"


class ColorFormatter(logging.Formatter):
    def __init__(self, default):
        super(ColorFormatter, self).__init__(fmt=default)
        self.default = default

    def format(self, record):
        formatted_text = super(ColorFormatter, self).format(record)
        seq_color = COLOR_SEQ % (30 + COLORS[record.levelname])
        formatted_text = "{}{}{}".format(seq_color, formatted_text, RESET_SEQ)
        return formatted_text


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id()
        return True


LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': RequestIdFilter,
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s.%(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(request_id)s - %(message)s',
        },
        'custom': {
            '()': ColorFormatter,
            'default': '%(asctime)s - %(name)s.%(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(request_id)s - %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'custom'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)
