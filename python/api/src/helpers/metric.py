import time
from contextlib import contextmanager

from flask import current_app


def _log_metric(grep_key, text_payload):
    current_app.logger.info("METRIC {}:{}".format(grep_key, text_payload))


@contextmanager
def timer(name):
    start = time.time()
    yield
    end = time.time()
    _log_metric("TIMER", "{} - {} s".format(name, (end - start)))


def count(event_name, payload):
    payload = payload if payload else {}
    payload.update({
        'event_time': time.time(),
    })
    _log_metric("COUNT", "{} - {}".format(event_name.value, payload))
