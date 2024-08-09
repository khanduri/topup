from ..mongo.topup import Beneficiary


class BeneficiaryDepot(object):

    @classmethod
    def create_beneficiary(cls, organization_xid, user_xid, data):
        return Beneficiary.create_beneficiary(organization_xid, user_xid, data)
    
    @classmethod
    def update_beneficiary(cls, organization_xid, user_xid,  beneficiary_xid, activate):
        data = {'active': activate}
        return Beneficiary.update_beneficiary(organization_xid, user_xid, beneficiary_xid, data)
    
    @classmethod
    def delete_beneficiaries(cls, organization_xid, user_xid):
        return Beneficiary.delete_beneficiaries(organization_xid, user_xid)

    @classmethod
    def select_beneficiaries(cls, organization_xid, user_xid):
        data = Beneficiary.select_beneficiaries(organization_xid, user_xid)
        return data
