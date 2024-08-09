from src.depot.topup.user_details import UserDetailsDepot

from src.micro_services.topup.constants import (
    ActionEnum, 
)

from .executor import ExecutorLogic

class UserTopUpLogic(object):
    
    @classmethod
    def reset_user_details(cls, organization_xid, user_xid):
        UserDetailsDepot.delete_user_state(organization_xid, user_xid)
        UserDetailsDepot.delete_user_activities(organization_xid, user_xid)

    @classmethod
    def fetch_user_details(cls, organization_xid, user_xid, range=None):

        user_state = UserDetailsDepot.select_user_state(organization_xid, user_xid)
        user_activities = UserDetailsDepot.select_user_activities(organization_xid, user_xid, range=range)

        payload = {
            'organization_xid': organization_xid,
            'user_xid': user_xid, 
            'user_state': user_state,
            'user_activities': user_activities,
        }

        return payload

    @classmethod
    def update_user_details(cls, organization_xid, user_xid, action, action_data):
        if (action in [ActionEnum.VERIFY_USER.name, ActionEnum.BALANCE_ADD.name]):
            return ExecutorLogic.execute_activity(organization_xid, user_xid, action, action_data)
