from flask import request

from src import topup_api_v1_bp
from src.helpers import api_response
from src.helpers.constants import Reason
from src.helpers.token_auth import user_auth_token_required
from src.micro_services.topup import logic


##################################################################
# Beneficiary REST Resource
##################################################################
@topup_api_v1_bp.route('/beneficiary', methods=['GET'])
@user_auth_token_required
def get_beneficiary(payload):
    organization_xid = payload['organization_xid']
    user_xid = payload['user_xid']
    
    payload = logic.BeneficiaryLogic.fetch_beneficiaries(organization_xid, user_xid)
    if not payload:
        return api_response.return_packet_fail(Reason.NOT_FOUND, message="Unable to find Beneficiaries!", response_code=406)
    
    return api_response.return_packet_success(payload)


@topup_api_v1_bp.route('/beneficiary', methods=['POST'])
@user_auth_token_required
def post_beneficiary(payload):
    organization_xid = payload['organization_xid']
    user_xid = payload['user_xid']
    data = request.json['data']
    
    payload = logic.BeneficiaryLogic.add_beneficiary(organization_xid, user_xid, data)

    return api_response.return_packet_success(payload, response_code=201)


@topup_api_v1_bp.route('/beneficiary/<beneficiary_xid>', methods=['POST'])
@user_auth_token_required
def post_beneficiary_topup(payload, beneficiary_xid):
    organization_xid = payload['organization_xid']
    user_xid = payload['user_xid']
    
    balance = request.json['balance']
    
    payload, error_reason = logic.BeneficiaryLogic.topup_beneficiary(organization_xid, user_xid, beneficiary_xid, balance)

    if error_reason:
        return api_response.return_packet_fail(Reason.INVALID, message=error_reason, response_code=400)

    return api_response.return_packet_success(payload)


@topup_api_v1_bp.route('/beneficiary/<beneficiary_xid>/activate', methods=['POST'])
@user_auth_token_required
def post_beneficiary_activate(payload, beneficiary_xid):
    organization_xid = payload['organization_xid']
    user_xid = payload['user_xid']

    activate = request.json['activate']
    
    payload, error_reason = logic.BeneficiaryLogic.update_beneficiary(organization_xid, user_xid, beneficiary_xid, activate)

    if error_reason:
        return api_response.return_packet_fail(Reason.INVALID, message=error_reason, response_code=400)

    return api_response.return_packet_success(payload)
