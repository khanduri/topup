from kombu import Queue
from celery import Celery
from celery.schedules import crontab

from src import create_app
from .constants import TaskQueue


def make_celery(app=None):
    app = app if app else create_app()
    _celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    _celery.conf.update(app.config)

    # https://stackoverflow.com/a/15827160/2069749
    _celery.conf.CELERY_DEFAULT_QUEUE = TaskQueue.DEFAULT
    _celery.conf.CELERY_QUEUES = (
        Queue(TaskQueue.DEFAULT),
        Queue(TaskQueue.LG_HIGH),
        Queue(TaskQueue.SM_HIGH),
        Queue(TaskQueue.LG_LOW),
        Queue(TaskQueue.SM_LOW),
    )

    # https://medium.com/the-andela-way/crontabs-in-celery-d779a8eb4cf
    _celery.conf.CELERYBEAT_SCHEDULE = {
        # 'every-minute-hello': {
        #     'schedule': crontab(minute="*"), 'task': 'task.services.temp.hello',
        # },
        'every-day-hello': {
            'schedule': crontab(hour="1", minute="7"), 'task': 'task.services.temp.hello',  # everyday@ 01:07am
        },
    }

    class ContextTask(_celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    _celery.Task = ContextTask

    return _celery
