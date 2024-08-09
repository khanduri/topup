from flask import request

from src import topup_api_v1_bp
from src.helpers import api_response
from src.helpers.constants import Reason
from src.helpers.token_auth import user_auth_token_required
from src.micro_services.topup import logic


##################################################################
# REST: TopUp User
##################################################################
@topup_api_v1_bp.route('/users', methods=['GET'])
@user_auth_token_required
def get_user_details(payload):
    organization_xid = payload['organization_xid']
    user_xid = payload['user_xid']
    
    payload = logic.UserTopUpLogic.fetch_user_details(organization_xid, user_xid)

    return api_response.return_packet_success(payload)


@topup_api_v1_bp.route('/users', methods=['POST'])
@user_auth_token_required
def post_user_details(payload):
    organization_xid = payload['organization_xid']
    user_xid = payload['user_xid']

    action = request.json['action']
    action_data = request.json['action_data']

    logic.UserTopUpLogic.update_user_details(organization_xid, user_xid, action, action_data)
    payload = logic.UserTopUpLogic.fetch_user_details(organization_xid, user_xid)
    
    return api_response.return_packet_success(payload)


