from enum import Enum


class EventBucket(Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'
    ERROR = 'error'


class EventService(Enum):
    SLACK = 'slack'             # Send a slack message
    AUDIT = 'audit'             # Record the event in the DB
    LOG = 'log'                 # Send a log about the event
    NOTIFY_SYS = 'notify_sys'   # Send an email to system admins
