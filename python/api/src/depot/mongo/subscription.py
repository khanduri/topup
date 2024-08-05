from .base import TableEnum, mongo_db
from .mixin import BaseMixin


class Subscription(BaseMixin):

    pattern = 'xxxxxxxxxxxxxxxxxxxx'

    _table_name = TableEnum.SUBSCRIPTION.name

    @classmethod
    def create_subscription(cls, email, meta, data):

        insert_data = cls._gen_insert_base()
        insert_data.update({
          'email': email,
          'meta': meta, 
          'data': data,
        })

        mongo_db(cls._table_name).insert_one(insert_data)
        return insert_data['xid']

    @classmethod
    def select_subscriptions(cls):
        search_criteria = {
            "removed_at": None,
        }
        # if service_xids:
        #     search_criteria.update({'xid': {'$in': service_xids}})

        logs = mongo_db(cls._table_name).find(search_criteria, {"_id": 0}) \
            .sort("_id", -1) \
            .limit(200)  # TODO: remove the limit and replace with advanced search support

        return [l for l in logs]
