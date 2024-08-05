from flask import current_app

from . import slack
from . import notify_sys
from . import audit
from .constants import EventBucket, EventService


class EventABC(object):
    event_bucket = EventBucket.DEBUG
    event_topic = 'GENERIC_TOPIC'
    event_text = 'GENERIC_EVENT_TEXT'

    __required_meta__ = []

    def __init__(self, event_text, **meta_dict):
        self.event_text = event_text
        for req in self.__required_meta__:
            assert req in meta_dict
        self.meta_dict = meta_dict

    def trigger(self, services):

        for service in services:

            if service == EventService.SLACK:
                slack.notify(self.event_bucket, self.event_topic, self.event_text, self.meta_dict)

            if service == EventService.NOTIFY_SYS:
                notify_sys.notify(self.event_bucket, self.event_topic, self.event_text, self.meta_dict)

            if service == EventService.AUDIT:
                audit.record(self.event_bucket.value, self.event_topic, self.event_text, self.meta_dict)

            if service == EventService.LOG:
                topic_msg = "{} - {} - {}".format(self.event_bucket, self.event_topic, self.event_text)
                meta_msg_list = [" - {}: {} ".format(k, v) for k, v in self.meta_dict.items()]
                meta_msg = "\n".join([m for m in meta_msg_list])

                logger_fn = {
                    EventBucket.ERROR:  current_app.logger.error,
                    EventBucket.CRITICAL:  current_app.logger.warning,
                    EventBucket.WARNING: current_app.logger.warning,
                    EventBucket.INFO:  current_app.logger.info,
                    EventBucket.DEBUG:  current_app.logger.info,
                }.get(self.event_bucket, current_app.logger.info)

                logger_fn(topic_msg)
                logger_fn(meta_msg)


class PreCreateEvent(EventABC):
    event_bucket = EventBucket.CRITICAL
    event_topic = 'PRE_CREATE_ACTION'


class CreateEntityEvent(EventABC):
    event_bucket = EventBucket.CRITICAL
    event_topic = 'CREATE_ENTITY_ACTION'


class PostCreateEvent(EventABC):
    event_bucket = EventBucket.CRITICAL
    event_topic = 'POST_CREATE_ACTION'
    __required_meta__ = ['oxid']


class AdminEvent(EventABC):
    event_bucket = EventBucket.CRITICAL
    event_topic = 'ADMIN_ACTION'
    __required_meta__ = ['uxid']


class UserEvent(EventABC):
    event_bucket = EventBucket.INFO
    event_topic = 'USER_ACTION'
    __required_meta__ = ['oxid', 'uxid']


class SystemEvent(EventABC):
    event_bucket = EventBucket.INFO
    event_topic = 'SYSTEM_ACTION'
