from ..mongo.topup import UserTransaction


class UserTransactionDepot(object):

    @classmethod
    def transfer_balance(cls, organization_xid, user_xid, beneficiary_xid, amount, fees):
        UserTransaction.transfer_balance(organization_xid, user_xid, beneficiary_xid, amount, fees)
