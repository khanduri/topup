from ..mongo.topup import UserActivity, UserState


class UserDetailsDepot(object):

    @classmethod
    def update_user_state(cls, organization_xid, user_xid, data):
        xid = UserState.update_user_state(organization_xid, user_xid, data)
        return xid  
    
    @classmethod
    def inc_user_balance(cls, organization_xid, user_xid, amount):
        return UserState.inc_user_balance(organization_xid, user_xid, amount)

    @classmethod
    def select_user_state(cls, organization_xid, user_xid):
        data = UserState.select_user_state(organization_xid, user_xid)
        return data or {}

    @classmethod
    def delete_user_state(cls, organization_xid, user_xid):
        UserState.delete_user_state(organization_xid, user_xid)
    
    @classmethod
    def delete_user_activities(cls, organization_xid, user_xid):
        UserActivity.delete_user_activity(organization_xid, user_xid)

    @classmethod
    def create_user_activity(cls, organization_xid, user_xid, data):
        xid = UserActivity.create_user_activity(organization_xid, user_xid, data)
        return xid

    @classmethod
    def select_user_activities(cls, organization_xid, user_xid, range=None):
        data = UserActivity.select_user_activities(organization_xid, user_xid, range=range)
        return data or []
