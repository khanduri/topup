from src.micro_services.topup.constants import (
    ActionEnum, 
    TOPUP_FEES, 
)

from .executor import ExecutorLogic
from .user import UserTopUpLogic
from .beneficiary import BeneficiaryLogic

class SetupLogic(object):

    @classmethod
    def run_clean_slate(cls, organization_xid, user_xid):
        SetupLogic.run_full_reset(organization_xid, user_xid)

    @classmethod
    def run_full_reset(cls, organization_xid, user_xid):
        UserTopUpLogic.reset_user_details(organization_xid, user_xid)
        BeneficiaryLogic.remove_beneficiaries(organization_xid, user_xid)
    
    @classmethod
    def run_bootstrap(cls, organization_xid, user_xid):
        cls.run_full_reset(organization_xid, user_xid)
        
        ExecutorLogic.execute_activity(organization_xid, user_xid, ActionEnum.BALANCE_ADD.name, 50000)
        # ExecutorLogic.execute_activity(organization_xid, user_xid, ActionEnum.VERIFY_USER.name, False)

        members = [
            {"nickname": "Prashant Khanduri", "email": "prashant.khanduri@gmail.com", "balance": 0},
            {"nickname": "Layla Al-Nuaimi", "email": "layla.alnuaimi@example.com", 'active': False, "balance": 400},
            {"nickname": "Maria Gomez", "email": "maria.gomez@example.com", "balance": 485},
            {"nickname": "Omar Al-Jabri", "email": "omar.aljabri@example.com", "balance": 50},
            {"nickname": "Jenna Williams", "email": "jenna.williams@example.com", "balance": 180},
            {"nickname": "Raj Patel", "email": "raj.patel@example.com", 'active': False, "balance": 75},
            {"nickname": "Fatima Al-Sabah", "email": "fatima.alsabah@example.com", "balance": 310},
            {"nickname": "Hina Rahman", "email": "hina.rahman@example.com", "balance": 275},
        ]
        for m in members:
            data = BeneficiaryLogic.add_beneficiary(organization_xid, user_xid, m)
            m['xid'] = data['xid']

        for idx in range(4):
            topup_member = members[idx]
            ExecutorLogic.execute_activity(organization_xid, user_xid, ActionEnum.BENEFICIARY_CREDIT.name, {'beneficiary_xid': topup_member['xid'], 'amount': 20, 'fees': TOPUP_FEES,})
