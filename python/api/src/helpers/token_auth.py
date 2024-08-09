import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, request

from .api_response import return_packet_fail
from .constants import Reason

from src.helpers.constants import get_app_constant
from src.helpers import metric
# from src.helpers.events import EventService, PostCreateEvent


_blocked_organizations = {
}

_whitelisted_organizations = {
}

_blocked_users = {
}


def _decode_token(token, secret_key, leeway=0):
    return jwt.decode(token, secret_key, algorithms=['HS256'], leeway=leeway)


def _encode_token(payload, secret_key):
    return jwt.encode(payload, secret_key, algorithm='HS256')
    # return jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    


def encode_user_auth_token(payload, expires_in=60*60*24*int(os.environ.get("CONST_UX_USER_AUTH_TOKEN_EXPIRE_DAY_COUNT", 1))):
    """

    :param payload:
    :param expires_in: default expiry in 12 hours (60 sec * 60 min * 24 hours) * 1
    :return:
    """
    secret_key = current_app.config['USER_AUTH_SECRET_KEY']
    payload.update({'exp': datetime.utcnow() + timedelta(seconds=expires_in)})
    return _encode_token(payload, secret_key)


def user_auth_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get('Authorization')
        # token = auth_header.split(" ")[1] if auth_header else None
        auth_sections = auth_header.split(" ") if auth_header else []

        if len(auth_sections) == 2:
            token = auth_sections[1]
            leeway = 0
        elif len(auth_sections) == 3:
            token = auth_sections[1]
            # 1 year leeway
            leeway = 60*60*24*365 if auth_sections[2] == 'simulation' else 0
        else:
            token = None

        if token == 'BYPASS_AUTH_FOR_NOW' and (current_app.config["DEVELOPMENT"] or current_app.config["TESTING"]):
            # Bypassing auth should NEVER happen on LIVE OR STAGE! Designed for Dev!
            payload = {
                'organization_xid': 'app_public_org_xid',
                'user_xid': 'UNKNOWN_USER_FOR_BYPASS_AUTH'
            }
            return f(payload, *args, **kwargs)

        if not token:
            return return_packet_fail(Reason.TOKEN_MISSING, response_code=401)

        secret_key = current_app.config['USER_AUTH_SECRET_KEY']
        try:
            payload = _decode_token(token.strip('"'), secret_key, leeway=leeway)
            oxid = payload['organization_xid']
            uxid = payload['user_xid']

            if os.environ['TARGET_SUB_DOMAIN'] == 'app':
                if not current_app.config["DEVELOPMENT"] and payload.get('organization_xid') not in _whitelisted_organizations:
                    # PostCreateEvent('ORGANIZATION_STOP', oxid=oxid, uxid=uxid).trigger([EventService.SLACK, EventService.NOTIFY_SYS])
                    return return_packet_fail(Reason.ORGANIZATION_STOP, response_code=403)

                if payload.get('organization_xid') in _blocked_organizations:
                    # PostCreateEvent('ORGANIZATION_PILOT_COMPLETE', oxid=oxid, uxid=uxid).trigger([EventService.SLACK, EventService.NOTIFY_SYS])
                    return return_packet_fail(Reason.ORGANIZATION_PILOT_COMPLETE, response_code=403)

                if payload.get('user_xid') in _blocked_users:
                    # PostCreateEvent('USER_PILOT_COMPLETE', oxid=oxid, uxid=uxid).trigger([EventService.SLACK, EventService.NOTIFY_SYS])
                    return return_packet_fail(Reason.USER_PILOT_COMPLETE, response_code=403)
        except:
            return return_packet_fail(Reason.TOKEN_INVALID, response_code=401)

        # logging.debug_log("Calling fn: {}".format(f.__name__))
        if get_app_constant('CONST_DISABLE_TIMER_LOGS', True):
            return f(payload, *args, **kwargs)
        else:
            with metric.timer("USER_AUTH {}".format(f.__name__)):
                return f(payload, *args, **kwargs)

    return decorated


def create_user_token_payload(user_xid, organization_xid):
    payload = {
        'target': os.environ['TARGET_SUB_DOMAIN'],
        'user_xid': user_xid,
        'organization_xid': organization_xid,
    }
    return payload
