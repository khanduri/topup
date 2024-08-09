from src.depot.topup.beneficiary import BeneficiaryDepot
from src.depot.topup.user_details import UserDetailsDepot
from src.depot.topup.transactions import UserTransactionDepot

from src.micro_services.topup.constants import (
    ActionEnum, 
)

class ExecutorLogic(object):

    @classmethod
    def execute_activity(cls, organization_xid, user_xid, action, action_data):

        UserDetailsDepot.create_user_activity(organization_xid, user_xid, {'action':action, 'action_data': action_data})

        if (action == ActionEnum.VERIFY_USER.name):
            UserDetailsDepot.update_user_state(organization_xid, user_xid, {'verified': action_data})

        if (action == ActionEnum.BALANCE_ADD.name):
            UserDetailsDepot.inc_user_balance(organization_xid, user_xid, action_data)

        if (action == ActionEnum.BENEFICIARY_CREDIT.name):
            beneficiary_xid = action_data['beneficiary_xid']
            amount = action_data['amount']
            fees = action_data['fees']
            UserTransactionDepot.transfer_balance(organization_xid, user_xid, beneficiary_xid, amount, fees)
            
        if (action == ActionEnum.BENEFICIARY_ACTIVATE.name):
            beneficiary = BeneficiaryDepot.update_beneficiary(organization_xid, user_xid, beneficiary_xid, {'active': True})
        
        if (action == ActionEnum.BENEFICIARY_DEACTIVATE.name):
            beneficiary = BeneficiaryDepot.update_beneficiary(organization_xid, user_xid, beneficiary_xid, {'active': False})
        
        return
        

