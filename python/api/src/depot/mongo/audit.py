import pymongo

from .base import TableEnum, mongo_db
from .mixin import BaseMixin


class Audit(BaseMixin):

    pattern = 'xxxxxxxxxxxxxxxxxxxxxx'
    _table_name = TableEnum.AUDIT.name

    @classmethod
    def indexes_create(cls):
        mongo_db(cls._table_name).create_index([
            ('xid', pymongo.ASCENDING),
        ], name='xid_1')

    @classmethod
    def insert_log(cls, bucket, topic, text, meta_dict):
        insert_data = cls._gen_insert_base()

        insert_data.update({
            'bucket': bucket,
            'topic': topic,
            'text': text,
            'meta_dict': meta_dict,
        })

        mongo_db(cls._table_name).insert_one(insert_data)
        del insert_data['_id']

        return insert_data

    @classmethod
    def fetch_logs(cls):
        search_criteria = {
            "removed_at": None,
        }
        # if service_xids:
        #     search_criteria.update({'xid': {'$in': service_xids}})

        logs = mongo_db(cls._table_name).find(search_criteria, {"_id": 0})\
            .sort("_id", -1) \
            .limit(200)  # TODO: remove the limit and replace with advanced search support

        return [l for l in logs]
