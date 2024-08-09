import datetime
import pymongo

from .base import TableEnum, mongo_db
from .mixin import BaseMixin


class User(BaseMixin):

    pattern = 'xxxx_xxxx_xxxx'

    _table_name = TableEnum.USER.name

    @classmethod
    def indexes_create(cls):
        mongo_db(cls._table_name).create_index([
            ('organization_xid', pymongo.ASCENDING),
            ('xid', pymongo.ASCENDING),
        ], name='oxid_u_1')

    @classmethod
    def create_user(cls, organization_xid, username, email):

        insert_data = cls._gen_insert_base()
        insert_data.update({
            'organization_xid': organization_xid,
            'username': username,
            'email': email,
        })

        mongo_db(cls._table_name).insert_one(insert_data)
        return insert_data

    @classmethod
    def select_by(cls, organization_xid=None, user_xids=None, emails=None):
        search_criteria = {
        }
        if organization_xid:
            search_criteria.update({'organization_xid': organization_xid})
        if user_xids:
            search_criteria.update({'xid': {'$in': user_xids}})
        if emails:
            search_criteria.update({'email': {'$in': emails}})

        results = [a for a in mongo_db(cls._table_name).find(search_criteria, {"_id": 0})]

        return results

    @classmethod
    def update_organization(cls, user_xid, organization_xid):
        search_criteria = {
            'xid': user_xid,
        }
        update = {
            "$set": {"organization_xid": organization_xid},
        }
        mongo_db(cls._table_name).update(search_criteria, update)

    @classmethod
    def delete_user(cls, user_xid):
        deletion_criteria = {
            'xid': user_xid,
        }
        query_exec = mongo_db(cls._table_name).delete_many(deletion_criteria)
        return query_exec.deleted_count


class UserSocial(BaseMixin):

    pattern = 'xxxxxxxxxxxxxxxxxxxx'

    _table_name = TableEnum.USER_SOCIAL.name

    @classmethod
    def indexes_create(cls):
        mongo_db(cls._table_name).create_index([
            ('organization_xid', pymongo.ASCENDING),
            ('user_xid', pymongo.ASCENDING),
        ], name='oxid_u_1')

    @classmethod
    def create_user_social(cls, organization_xid, user_xid, social_network, social_id, access_code):

        insert_data = cls._gen_insert_base()
        insert_data.update({
            'organization_xid': organization_xid,
            'user_xid': user_xid,
            'social_network': social_network,
            'social_id': social_id,
            'access_code': access_code,
        })

        mongo_db(cls._table_name).insert_one(insert_data)
        return insert_data

    @classmethod
    def update_social_access_code(cls, user_xid, social_network, social_id, access_code):
        search_criteria = {
            'user_xid': user_xid,
            'social_network': social_network,
            'social_id': social_id,
        }
        update = {
            "$set": {"access_code": access_code},
        }
        mongo_db(cls._table_name).update_one(search_criteria, update)

    @classmethod
    def update_organization(cls, user_xid, organization_xid):
        search_criteria = {
            'user_xid': user_xid,
        }
        update = {
            "$set": {"organization_xid": organization_xid},
        }
        mongo_db(cls._table_name).update(search_criteria, update)

    @classmethod
    def select_by(cls, social_network=None, social_id=None, user_xid=None):
        search_criteria = {
        }
        if social_network:
            search_criteria.update({'social_network': social_network})
        if social_id:
            search_criteria.update({'social_id': social_id})
        if user_xid:
            search_criteria.update({'user_xid': user_xid})
        results = [a for a in mongo_db(cls._table_name).find(search_criteria, {"_id": 0})]
        return results[0] if results else None

    @classmethod
    def delete_user_social(cls, user_xid):
        deletion_criteria = {
            'user_xid': user_xid,
        }
        query_exec = mongo_db(cls._table_name).delete_many(deletion_criteria)
        return query_exec.deleted_count


class UserEmailLogin(BaseMixin):

    pattern = 'xxxx_xxxx_xxxx'

    _table_name = TableEnum.USER_LOGIN_CODE.name

    @classmethod
    def indexes_create(cls):
        mongo_db(cls._table_name).create_index([
            ('organization_xid', pymongo.ASCENDING),
            ('email', pymongo.ASCENDING),
        ], name='oxid_em_1')

    @classmethod
    def create_email_login_code(cls, organization_xid, email):

        insert_data = cls._gen_insert_base()
        login_code = cls.gen_xid(pattern='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        valid_until = datetime.datetime.utcnow() + datetime.timedelta(days=30, hours=24, minutes=30)
        insert_data.update({
            'organization_xid': organization_xid,
            'email': email,
            'login_code': login_code,
            'valid_until': valid_until,
        })

        mongo_db(cls._table_name).insert_one(insert_data)
        return insert_data

    @classmethod
    def select_email_login_code(cls, organization_xid, email):
        current_time = datetime.datetime.utcnow()
        search_criteria = {
            'organization_xid': organization_xid,
            "email": email,
            'valid_until': {'$gt': current_time}
        }
        results = [a for a in mongo_db(cls._table_name).find(search_criteria, {"_id": 0})]
        return results[0] if results else None


class Organization(BaseMixin):

    pattern = 'xxxx_xxxx'

    _table_name = TableEnum.ORGANIZATION.name

    @classmethod
    def indexes_create(cls):
        mongo_db(cls._table_name).create_index([
            ('xid', pymongo.ASCENDING),
        ], name='oxid_1')

    @classmethod
    def create_organization(cls, name, domain):
        insert_data = cls._gen_insert_base()
        insert_data.update({
            'name': name,
            'domain': domain,
        })
        mongo_db(cls._table_name).insert_one(insert_data)
        del insert_data['_id']
        return insert_data

    @classmethod
    def fetch_by_domain(cls, domain):
        search_criteria = {
            "domain": domain,
        }
        results = [a for a in mongo_db(cls._table_name).find(search_criteria, {"_id": 0})]
        return results[0] if results else None
