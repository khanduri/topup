from src.depot.topup.beneficiary import BeneficiaryDepot

from src.micro_services.topup.utils import get_current_month_start_end
from src.micro_services.topup.constants import (
    ActionEnum, 
    TOPUP_FEES, 
    MAX_ACTIVE_BENEFICIARIES, 
    MAX_MONTHLY_LIMIT,
    MAX_BENEFICIARY_VERIFIED_LIMIT,
    MAX_BENEFICIARY_UNVERIFIED_LIMIT,
)
from .executor import ExecutorLogic
from .user  import UserTopUpLogic


class BeneficiaryLogic(object):

    @classmethod
    def add_beneficiary(cls, organization_xid, user_xid, data):
        nickname = data.get('nickname', "__")
        if len(nickname) > 20:
            return None
        
        result = cls.fetch_beneficiaries(organization_xid, user_xid)
        active = data['active'] if 'active'in data else (len([r for r in result['beneficiaries'] if r['data']['active']]) < MAX_ACTIVE_BENEFICIARIES)
        
        data_mod = {
            'nickname': nickname,
            'email': data['email'],
            'active': active,
            'balance': 0,
        }

        xid = BeneficiaryDepot.create_beneficiary(organization_xid, user_xid, data_mod)

        topup = int(data.get('balance', '0'))
        if topup and active:
            cls.topup_beneficiary(organization_xid, user_xid, xid, topup)

        return {'xid': xid, 'data':data_mod }
    
    @classmethod
    def update_beneficiary(cls, organization_xid, user_xid, beneficiary_xid, activate):
        result = cls.fetch_beneficiaries(organization_xid, user_xid)
        allowed = (len([r for r in result['beneficiaries'] if r['data']['active']]) < MAX_ACTIVE_BENEFICIARIES)

        if not allowed and activate:
            return None, "Exceeding active beneficiaries limit!"

        data = BeneficiaryDepot.update_beneficiary(organization_xid, user_xid,  beneficiary_xid, activate)
        return data, None
    
    @classmethod
    def remove_beneficiaries(cls, organization_xid, user_xid):
        return BeneficiaryDepot.delete_beneficiaries(organization_xid, user_xid)
    
    @classmethod
    def fetch_beneficiaries(cls, organization_xid, user_xid):
        
        beneficiaries = BeneficiaryDepot.select_beneficiaries(organization_xid, user_xid)

        result = {
            'organization_xid': organization_xid,
            'user_xid': user_xid, 
            'beneficiaries': beneficiaries,
        }
        return result

    @classmethod
    def topup_beneficiary(cls, organization_xid, user_xid, beneficiary_xid, topup_balance):

        start_time, end_time = get_current_month_start_end()
        user_details = UserTopUpLogic.fetch_user_details(organization_xid, user_xid, range=(start_time, end_time))
        user_state = user_details['user_state']

        user_balance = user_state['data'].get('balance', 0)
        topup_charge = topup_balance + TOPUP_FEES

        if (user_balance < topup_charge):
            return None, "Insufficient Balance!"
        
        user_activities = user_details['user_activities']
        credit_adds = [a for a in user_activities if a['data']['action'] == ActionEnum.BENEFICIARY_CREDIT.name]
        credit_map = {}
        total_credit = 0
        for ca in credit_adds:
            if not ca['data']['action_data']['beneficiary_xid'] in credit_map:
                credit_map[ca['data']['action_data']['beneficiary_xid']] = 0
            credit_map[ca['data']['action_data']['beneficiary_xid']] += ca['data']['action_data']['amount']
            total_credit += ca['data']['action_data']['amount']
        
        if total_credit + topup_charge > MAX_MONTHLY_LIMIT:
            return None, "Exceeding monthly limits!"
        
        verified = user_state['data'].get('verified', False)
        beneficiary_topup_history = credit_map.get(beneficiary_xid, 0)
        if verified and beneficiary_topup_history + topup_charge > MAX_BENEFICIARY_VERIFIED_LIMIT:
            return None, "Exceeding beneficiary limits! - Verified User"
        
        if not verified and beneficiary_topup_history + topup_charge > MAX_BENEFICIARY_UNVERIFIED_LIMIT:
            return None, "Exceeding beneficiary limits! - Unverified User"

        action_data = {
            'beneficiary_xid': beneficiary_xid,
            'amount': topup_balance,
            'fees': TOPUP_FEES,
        }
        ExecutorLogic.execute_activity(organization_xid, user_xid, ActionEnum.BENEFICIARY_CREDIT.name, action_data)
        
        return None, None



