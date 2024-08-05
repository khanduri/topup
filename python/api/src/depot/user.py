from .mongo.user import UserEmailLogin, User, UserSocial
from .mongo.user import Organization


class OrganizationDepot(object):

    @classmethod
    def fetch_by_domain(cls, domain):
        return Organization.fetch_by_domain(domain)

    @classmethod
    def create_organization(cls, name, domain):
        return Organization.create_organization(name, domain)


class UserDepot(object):

    @classmethod
    def fetch_all_users(cls, organization_xid=None, user_xids=None, emails=None):
        users = User.select_by(organization_xid=organization_xid, user_xids=user_xids, emails=emails)
        return users

    @classmethod
    def fetch_user_social_by_social(cls, social_network, social_id):
        user_social = UserSocial.select_by(social_network=social_network, social_id=social_id)
        return user_social

    @classmethod
    def fetch_user_social_by_user_xid(cls, user_xid):
        user_social = UserSocial.select_by(user_xid=user_xid)
        return user_social

    @classmethod
    def fetch_user(cls, organization_xid, user_xid):
        user_list = User.select_by(organization_xid=organization_xid, user_xids=[user_xid])
        user = user_list[0] if user_list else None
        return user

    @classmethod
    def fetch_full_user(cls, organization_xid, user_xid):
        user_list = User.select_by(organization_xid=organization_xid, user_xids=[user_xid])
        user = user_list[0] if user_list else None
        user_social = UserSocial.select_by(user_xid)
        data = {
            'user': user,
            'user_social': user_social,
        }
        return data

    @classmethod
    def update_social_access_code(cls, user_xid, social_network, social_id, access_code):
        UserSocial.update_social_access_code(user_xid, social_network, social_id, access_code)

    @classmethod
    def create_organization_user(cls, org_xid, username, email, social_network, social_id, access_code):
        user = User.create_user(org_xid, username, email)
        user_xid = user['xid']
        UserSocial.create_user_social(org_xid, user_xid, social_network, social_id, access_code)
        return user


class UserEmailLoginDepot(object):

    @classmethod
    def create_login_code(cls, organization_xid, email):
        login_code_data = cls.select_login_code(organization_xid, email)
        if not login_code_data:
            login_code_data = UserEmailLogin.create_email_login_code(organization_xid, email)
        return login_code_data

    @classmethod
    def select_login_code(cls, organization_xid, email):
        login_code_data = UserEmailLogin.select_email_login_code(organization_xid, email)
        return login_code_data
