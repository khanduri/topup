import datetime
import random
import string

from src.depot.mongo.base import mongo_db


class BaseMixin(object):

    pattern = 'xxxxxx_xxxxxx_xxxxxx'

    _table_name = None

    @classmethod
    def gen_xid(cls, pattern="xxxx_xxxx_xxxx"):
        alphabet = string.ascii_lowercase + string.digits
        chunks = pattern.split("_")
        return '_'.join([''.join(random.choices(alphabet, k=len(chunk))) for chunk in chunks])

    @classmethod
    def _gen_insert_base(cls):
        return {
            'xid': cls.gen_xid(cls.pattern),
            "removed_at": None,
            "inserted_at": datetime.datetime.utcnow().timestamp() * 1000,
        }

    @classmethod
    def drop_indexes(cls, indexes):
        for drop_index_name in indexes:
            mongo_db(cls._table_name).drop_index(drop_index_name)

    @classmethod
    def indexes_select(cls):
        # https://www.analyticsvidhya.com/blog/2020/09/mongodb-indexes-pymongo-tutorial/
        index_info = mongo_db(cls._table_name).index_information()
        return index_info


class DeleteSupportMixin(object):

    @property
    def _table_name(self):
        raise NotImplementedError

    @classmethod
    def hard_delete_all(cls):
        deletion_criteria = {}
        query_exec = mongo_db(cls._table_name).delete_many(deletion_criteria)
        return query_exec.deleted_count

    @classmethod
    def drop_table(cls):
        mongo_db(cls._table_name).drop()


class StaleSupportMixin(object):

    @property
    def _table_name(self):
        raise NotImplementedError

    @classmethod
    def delete_stale_data(cls, remove_time):
        query_exec = mongo_db(cls._table_name).delete_many(
            {"$or": [{'inserted_at': {"$lte": remove_time, }}, {"removed_at": {"$ne": None}}, {'inserted_at': None}]})
        return query_exec.deleted_count
