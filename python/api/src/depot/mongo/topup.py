import os 
import datetime
import pymongo
from pymongo import MongoClient
from flask import current_app

from src import mongo

from .base import TableEnum, mongo_db
from .mixin import BaseMixin


_client = None
class UserTransaction():

    @classmethod
    def transfer_balance(cls, organization_xid, user_xid, beneficiary_xid, amount, fees):
        
        def callback(
            session,
            organization_xid=None, 
            user_xid=None, 
            beneficiary_xid=None, 
            amount=None,
            fees=None,
        ):
            db_name = os.environ.get('MONGO_DB', 'skeleton-dev')
            tus_coll = session.client.get_database(db_name).topup_user_state
            b_coll = session.client.get_database(db_name).topup_beneficiary

            resp = tus_coll.update_one(
                {
                    "organization_xid": organization_xid,
                    "user_xid": user_xid,
                },
                {
                    "$inc": {"data.balance": -(amount+fees)},
                },
                session=session,
                upsert=True,
            )

            b_coll.update_one(
                {
                    "organization_xid": organization_xid,
                    "user_xid": user_xid,
                    "xid": beneficiary_xid,
                },
                {
                    "$inc": {"data.balance": amount},
                },
                session=session,
                upsert=True,
            )
            return

        def callback_wrapper(s):
            callback(
                s,
                organization_xid=organization_xid, 
                user_xid=user_xid, 
                beneficiary_xid=beneficiary_xid, 
                amount=amount,
                fees=fees,
            )

        global _client
        if not _client:
            _client = MongoClient(current_app.config["MONGO_URI"])
        with _client.start_session() as session:
            session.with_transaction(callback_wrapper)


class UserState(BaseMixin):

    pattern = 'xxxx_xxxxxxxx'

    _table_name = TableEnum.TOPUP_USER_STATE.name

    @classmethod
    def indexes_create(cls):
        mongo_db(cls._table_name).create_index([
            ('organization_xid', pymongo.ASCENDING),
            ('user_xid', pymongo.ASCENDING),
        ], name='oxid_uxid_1')

    @classmethod
    def update_user_state(cls, organization_xid, user_xid, data):
        search_criteria = {
            'organization_xid': organization_xid,
            'user_xid': user_xid,
        }
        updated_data = {}
        if 'verified' in data:
            updated_data = {'data.verified': data['verified']}
        if 'balance' in data:
            updated_data = {'data.balance': data['balance']}

        update = {
            "$set": updated_data,
        }
        mongo_db(cls._table_name).update_one(search_criteria, update, upsert=True)

    @classmethod
    def inc_user_balance(cls, organization_xid, user_xid, amount):
        search_criteria = {
            'organization_xid': organization_xid,
            'user_xid': user_xid,
        }
        update = {
            "$inc": {"data.balance": amount},
        }
        mongo_db(cls._table_name).update_one(search_criteria, update, upsert=True)
        

    @classmethod
    def delete_user_state(cls, organization_xid, user_xid):
        search_criteria = {
            'organization_xid': organization_xid,
            'user_xid': user_xid,
        }
        update = {
            "$set": {"data": {}},
        }
        mongo_db(cls._table_name).update_one(search_criteria, update)

    @classmethod
    def select_user_state(cls, organization_xid, user_xid):
        search_criteria = {
            'organization_xid': organization_xid, 
            'user_xid': user_xid,
        }
     
        results = [a for a in mongo_db(cls._table_name).find(search_criteria, {"_id": 0})]
        return results[0] if results else None


class UserActivity(BaseMixin):

    pattern = 'xxxx_xxxx_xxxx_xxxx'

    _table_name = TableEnum.TOPUP_USER_ACTIVITY.name

    @classmethod
    def indexes_create(cls):
        mongo_db(cls._table_name).create_index([
            ('organization_xid', pymongo.ASCENDING),
            ('user_xid', pymongo.ASCENDING),
        ], name='oxid_uxid_1')

    @classmethod
    def create_user_activity(cls, organization_xid, user_xid, data):

        insert_data = cls._gen_insert_base()
        insert_data.update({
            'organization_xid': organization_xid,
            'user_xid': user_xid,
            'data': data,
        })

        mongo_db(cls._table_name).insert_one(insert_data)
        return insert_data

    @classmethod
    def delete_user_activity(cls, organization_xid, user_xid):
        search_criteria = {
            'organization_xid': organization_xid, 
            'user_xid': user_xid,
        }
        return mongo_db(cls._table_name).delete_many(search_criteria)

    @classmethod
    def select_user_activities(cls, organization_xid, user_xid, range=None):
        search_criteria = {
            'organization_xid': organization_xid, 
            'user_xid': user_xid,
        }
        if range:
            search_criteria['inserted_at'] = {
                '$gte': range[0],
                '$lt': range[1]
            }

        print(search_criteria)
        results = [a for a in mongo_db(cls._table_name).find(search_criteria, {"_id": 0})]
        return results


class Beneficiary(BaseMixin):

    pattern = 'xxxx_xxxx_xxxx_xxxx'

    _table_name = TableEnum.TOPUP_BENEFICIARY.name

    @classmethod
    def indexes_create(cls):
        mongo_db(cls._table_name).create_index([
            ('organization_xid', pymongo.ASCENDING),
            ('user_xid', pymongo.ASCENDING),
        ], name='oxid_uxid_1')

    @classmethod
    def create_beneficiary(cls, organization_xid, user_xid, data):

        insert_data = cls._gen_insert_base()
        insert_data.update({
            'organization_xid': organization_xid,
            'user_xid': user_xid,
            'data': data,
        })

        mongo_db(cls._table_name).insert_one(insert_data)
        return insert_data['xid']
    
    @classmethod
    def delete_beneficiaries(cls, organization_xid, user_xid):
        search_criteria = {
            'organization_xid': organization_xid, 
            'user_xid': user_xid,
        }
        return mongo_db(cls._table_name).delete_many(search_criteria)

    @classmethod
    def update_beneficiary(cls, organization_xid, user_xid, beneficiary_xid, data):
        search_criteria = {
            'organization_xid': organization_xid,
            'user_xid': user_xid,
            'xid': beneficiary_xid,
        }
        updated_data = {}
        if 'active' in data:
            updated_data = {'data.active': data['active']}

        update = {
            "$set": updated_data,
        }
        print(search_criteria)
        print(update)
        mongo_db(cls._table_name).update_one(search_criteria, update)
        
    @classmethod
    def select_beneficiaries(cls, organization_xid, user_xid):
        search_criteria = {
            'organization_xid': organization_xid, 
            'user_xid': user_xid,
        }
        results = [a for a in mongo_db(cls._table_name).find(search_criteria, {"_id": 0})]
        return results