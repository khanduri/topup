from flask import request

from src import users_api_v1_bp
from src.helpers import api_response
from src.helpers.events import EventService, AdminEvent
from src.helpers.token_auth import user_auth_token_required
from src.micro_services.users import logic


##################################################################
# DEBUG / TEST API
##################################################################
@users_api_v1_bp.route('/ping', methods=['GET'])
def get_ping():
    return api_response.return_packet_success({'ack': 'ok'})


##################################################################
# Login API
##################################################################
@users_api_v1_bp.route('/login/email', methods=['POST'])
def login_email():
    invite_code = request.json.get('invite_code')
    work_email = request.json.get('work_email', '')

    if invite_code:
        payload, reason, msg = logic.validate_invite_code(work_email, invite_code)
        if not payload:
            return api_response.return_packet_fail(reason, message=msg)

        return api_response.return_packet_success(payload)

    validated_email = logic.validate_email_and_send_login_code(work_email)

    # NOTE: don't reply back with a confirmation on validation of any email address. This
    # can leak information about emails / accounts
    # if not validated_email:
    # return api_response.return_packet_fail(Reason.INVITE_EMAIL_INVALID)
    return api_response.return_packet_success({})


@users_api_v1_bp.route('/auth/google', methods=['POST'])
def grant_jwt_token_for_google_auth():

    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1] if auth_header else None

    user_oauth_model, reason, msg = logic.fetch_user_auth_model(access_token)
    if not user_oauth_model:
        return api_response.return_packet_fail(reason, message=msg)

    payload, reason, msg = logic.fetch_user_auth_token(user_oauth_model)
    if not payload:
        return api_response.return_packet_fail(reason, message=msg)

    return api_response.return_packet_success(payload)


##################################################################
# ADMIN API
##################################################################
@users_api_v1_bp.route('/sysadmin', methods=['GET'])
@user_auth_token_required
def get_user_admin(payload):
    user_xid = payload['user_xid']
    organization_xid = payload['organization_xid']
    is_admin = logic.is_user_admin(organization_xid, user_xid)
    return api_response.return_packet_success(is_admin)


##################################################################
# GHOST API
##################################################################
@users_api_v1_bp.route('/ghost', methods=['GET'])
@user_auth_token_required
def get_user_ghosting_allowed(payload):
    user_xid = payload['user_xid']
    organization_xid = payload['organization_xid']

    is_admin, grouped_users = logic.fetch_all_system_users_for_admin(organization_xid, user_xid)

    if not is_admin:
        return api_response.return_packet_success({})

    data = {
        'ghosting_allowed': is_admin,
        # 'user_list': users,
        'grouped_user_list': grouped_users,
    }

    return api_response.return_packet_success(data)


@users_api_v1_bp.route('/ghost', methods=['POST'])
@user_auth_token_required
def post_user_ghosting(payload):
    user_xid = payload['user_xid']
    organization_xid = payload['organization_xid']

    post_data = request.get_json()
    ghost_user_xid = post_data.get('ghost_user_xid')

    AdminEvent('GHOSTING_USER', uxid=user_xid, ghost=ghost_user_xid).trigger([EventService.SLACK, EventService.AUDIT])

    payload, reason, msg = logic.ghost_user(organization_xid, user_xid, ghost_user_xid)
    if not payload:
        return api_response.return_packet_fail(reason, message=msg)

    return api_response.return_packet_success(payload)


##################################################################
# USERS API
##################################################################
@users_api_v1_bp.route('/me', methods=['GET'])
@user_auth_token_required
def get_user_details(payload):
    user_xid = payload['user_xid']
    organization_xid = payload['organization_xid']
    data = logic.fetch_user(organization_xid, user_xid)
    return api_response.return_packet_success(data)
