import enum
from collections import namedtuple

from src import mongo


Table = namedtuple('Table', 'name')


class TableEnum(enum.Enum):
    AUDIT = Table('audit')

    SUBSCRIPTION = Table('subscription')
    FEEDBACK = Table('feedback')

    ORGANIZATION = Table('organization')

    USER = Table('user')
    USER_SOCIAL = Table('user_social')
    USER_LOGIN_CODE = Table('user_login_code')


_mongo_connections = {}


def mongo_db(collection_name):

    table_names = [a.name for a in TableEnum]
    if collection_name not in table_names:
        raise KeyError("Not a valid collection: {}". format(collection_name))

    global _mongo_connections
    if not _mongo_connections:
        _mongo_connections = {
            TableEnum.AUDIT.name:              mongo.db.audit,

            TableEnum.SUBSCRIPTION.name:       mongo.db.subscription,
            TableEnum.FEEDBACK.name:           mongo.db.feedback,

            # Product tables
            TableEnum.ORGANIZATION.name:       mongo.db.organization,

            TableEnum.USER.name:               mongo.db.user,
            TableEnum.USER_SOCIAL.name:        mongo.db.user_social,
            TableEnum.USER_LOGIN_CODE.name:    mongo.db.user_login_code,

        }
    return _mongo_connections[collection_name]


class StaleSupportMixin(object):

    @property
    def _table_name(self):
        raise NotImplementedError

    @classmethod
    def delete_stale_data(cls, remove_time):
        query_exec = mongo_db(cls._table_name).delete_many(
            {"$or": [{'inserted_at': {"$lte": remove_time, }}, {"removed_at": {"$ne": None}}, {'inserted_at': None}]})
        return query_exec.deleted_count
