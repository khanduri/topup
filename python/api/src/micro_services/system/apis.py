from flask import request

from src import generics_api_v1_bp, no_path_api_v1_bp
from src.helpers import api_response
from src.helpers.token_auth import user_auth_token_required
from src.micro_services.system import logic
from src.micro_services.users import logic as user_logic


##################################################################
# GENERIC / DEBUG / TEST API
##################################################################
@no_path_api_v1_bp.route('/', methods=['GET'])
def get_ping():
    return api_response.return_packet_success({"status": "good"})


@no_path_api_v1_bp.route('/exception', methods=['GET'])
def get_exception():
    raise NotImplementedError("You asked for an Exception!")


##################################################################
# GENERIC API
##################################################################
@generics_api_v1_bp.route('/feedback', methods=['POST'])
def feedback_submit():
    http_origin = request.environ.get('HTTP_ORIGIN', 'DEF_VAL')

    meta = {
        'http_origin': http_origin
    }
    data = request.json

    payload = logic.GenericsLogic.add_feedback(meta, data)
    return api_response.return_packet_success(payload)


@generics_api_v1_bp.route('/feedback', methods=['GET'])
@user_auth_token_required
def get_feedbacks(payload):
    user_xid = payload['user_xid']
    organization_xid = payload['organization_xid']
    payload = logic.GenericsLogic.fetch_feedback(organization_xid, user_xid)
    return api_response.return_packet_success(payload)


@generics_api_v1_bp.route('/subscribe', methods=['POST'])
def landing_subscribe():
    http_origin = request.environ.get('HTTP_ORIGIN', 'DEF_VAL')

    meta = {
        'http_origin': http_origin
    }
    data = request.json

    email = request.json['email']

    payload = logic.GenericsLogic.add_subscribe(email, meta, data)
    return api_response.return_packet_success(payload)


@generics_api_v1_bp.route('/subscribe', methods=['GET'])
@user_auth_token_required
def get_subscribes(payload):
    user_xid = payload['user_xid']
    organization_xid = payload['organization_xid']
    payload = logic.GenericsLogic.fetch_subscribe(organization_xid, user_xid)
    return api_response.return_packet_success(payload)


@generics_api_v1_bp.route('/index_details', methods=['GET'])
def indexes_details():
    passphrase = request.args.get('passphrase')
    if passphrase != 'enablegodmode':
        return api_response.return_packet_success({'run': "true"})

    return_packet = logic.MaintenanceLogic.maintenance_indexes_details()
    return api_response.return_packet_success(return_packet)


@generics_api_v1_bp.route('/index_details/create', methods=['GET'])
def indexes_create():
    passphrase = request.args.get('passphrase')
    if passphrase != 'enablegodmode':
        return api_response.return_packet_success({'run': "true"})

    block = request.args.get('block')
    return_packet = logic.MaintenanceLogic.maintenance_indexes_create(block)
    return api_response.return_packet_success(return_packet)


@generics_api_v1_bp.route('/info', methods=['GET'])
@user_auth_token_required
def get_system_info(payload):
    user_xid = payload['user_xid']
    organization_xid = payload['organization_xid']

    data = logic.fetch_system_info(organization_xid, user_xid)
    return api_response.return_packet_success(data)


@generics_api_v1_bp.route('/is_admin', methods=['GET'])
@user_auth_token_required
def get_is_admin(payload):
    user_xid = payload['user_xid']
    organization_xid = payload['organization_xid']

    data = user_logic.fetch_is_admin(organization_xid, user_xid)
    return api_response.return_packet_success(data)


@generics_api_v1_bp.route('/audit', methods=['GET'])
@user_auth_token_required
def get_system_audit_logs(payload):
    organization_xid = payload['organization_xid']
    user_xid = payload['user_xid']

    data = logic.fetch_system_audit_logs(organization_xid, user_xid)
    return api_response.return_packet_success(data)
