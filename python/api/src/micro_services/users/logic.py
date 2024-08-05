import os

from flask import current_app

from src.helpers.admin_auth import is_user_admin
from src.helpers.constants import Reason
from src.helpers.events import EventService, PreCreateEvent, UserEvent, SystemEvent, CreateEntityEvent
from src.helpers.oauth import GoogleSignIn, OAuth2Service
from src.helpers.token_auth import create_user_token_payload, encode_user_auth_token
from src.depot.user import UserEmailLoginDepot
from src.depot.user import OrganizationDepot
from src.depot.user import UserDepot
from src.micro_services.users.email import (
    send_email_login_code,
    # send_email_login_successful,
)
from src.helpers.oauth import UserOAuthModel


def fetch_user_auth_model(access_token):
    consumer_id = current_app.config['OAUTH_CREDENTIALS']['google']['id']
    consumer_secret = current_app.config['OAUTH_CREDENTIALS']['google']['secret']

    service = OAuth2Service(
        name='google',
        client_id=consumer_id,
        client_secret=consumer_secret,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        # base_url='https://www.googleapis.com/plus/v1/people/'
        base_url='https://www.googleapis.com/userinfo/v2/'
    )
    oauth_session = service.get_session(token=access_token)

    me = oauth_session.get('me').json()

    if 'error' in me:
        return None, Reason.SIGNIN_FAILED, me['error']['message']

    user_oauth_model = GoogleSignIn.parse_oauth_model(access_token, me)

    if user_oauth_model.social_id is None:
        return None, Reason.SIGNIN_FAILED, me['error']['message']

    return user_oauth_model, None, None


def _fetch_system_app(user_oauth_model):
    domain = 'system_public'
    org_model = OrganizationDepot.fetch_by_domain(domain)
    if not org_model:
        PreCreateEvent('ORGANIZATION_NOT_FOUND', domain=user_oauth_model.domain, email=user_oauth_model.email) \
            .trigger([EventService.SLACK, EventService.NOTIFY_SYS])
        name = 'system_app'
        org_model = OrganizationDepot.create_organization(name, domain)
    return domain, org_model, None


def _fetch_system_org(user_oauth_model):
    domain = _domain_overrides(user_oauth_model.email)
    if not domain:
        domain = user_oauth_model.domain

    org_model = OrganizationDepot.fetch_by_domain(domain)
    if not org_model:
        PreCreateEvent('ORGANIZATION_NOT_FOUND', domain=user_oauth_model.domain, email=user_oauth_model.email) \
            .trigger([EventService.SLACK, EventService.NOTIFY_SYS])
        if _is_domain_public(domain):
            return None, None, Reason.ORGANIZATION_NOT_WORK
        name = domain.split('.com')[0].capitalize()
        org_model = OrganizationDepot.create_organization(name, domain)
    return domain, org_model, None


def _fetch_system_dedicated(user_oauth_model):
    domain = _domain_overrides(user_oauth_model.email)
    if not domain:
        domain = user_oauth_model.domain

    org_model = OrganizationDepot.fetch_by_domain(domain)
    if not org_model:
        PreCreateEvent('ORGANIZATION_NOT_FOUND', domain=user_oauth_model.domain, email=user_oauth_model.email) \
            .trigger([EventService.SLACK, EventService.NOTIFY_SYS])
        # TODO: change name generation to EMAIL_DOMAINS: 'customer.com;domain1.com,domain2.com'
        # if domain not in os.environ['EMAIL_DOMAINS'].split(','):
        #     PreCreateEvent('ORGANIZATION_UNTARGETED', domain=domain, email=user_oauth_model.email)\
        #         .trigger([EventService.SLACK, EventService.NOTIFY_SYS])
        #     return None, None, Reason.ORGANIZATION_UNSCOPED
        name = 'EMAIL_DOMAINS'
        org_model = OrganizationDepot.create_organization(name, domain)
    return domain, org_model, None


def _is_domain_public(domain):
    # TODO: add more general mailing service domains in here
    # https://temporarymail.com
    public_domains = [
        'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.co', 'mail.com',
        'gmx.com', 'gmx.us', 'protonmail',

        # temporary email services
        'bcaoo.com', 'eoopy.com', 'zzrgg.com',  # https://10minutemail.net
        'earningsph.com',  # https://www.emailondeck.com
        'prowerl.com', 'whowlft.com', 'provlst.com',  # https://temp-mail.org/en/

        # https://www.guerrillamail.com
        "sharklasers.com", "guerrillamail.info", "grr.la", "guerrillamail.biz", "guerrillamail.com",
        "guerrillamail.de", "guerrillamail.net", "guerrillamail.org", "guerrillamailblock.com", "pokemail.net",
        "spam4.me",

        'andyes.net',  # https://www.fakemail.net/

        'byom.de',  # http://byom.de/

        'enayu.com',  # https://tempail.com/en/

        'wemel.site',  # https://www.throwawaymail.com/en

        'mailsy.top', 'zmexl@gurumail.xyz', 'wootap.me', 'senduvu.com',  # https://tempmailgen.com/
    ]
    return domain in public_domains


def fetch_user_auth_token(user_oauth_model):

    if os.environ['TARGET_SUB_DOMAIN'] in ['app']:
        domain, org_model, error = _fetch_system_app(user_oauth_model)
    elif os.environ['TARGET_SUB_DOMAIN'] in ['org']:
        domain, org_model, error = _fetch_system_org(user_oauth_model)
    else:
        domain, org_model, error = _fetch_system_dedicated(user_oauth_model)

    if error:
        return None, error, None

    if not org_model:
        PreCreateEvent('ORGANIZATION_NOT_REGISTERED', domain=domain, email=user_oauth_model.email)\
            .trigger([EventService.SLACK, EventService.NOTIFY_SYS])
        return None, Reason.ORGANIZATION_NOT_REGISTERED, None

    user_model = create_or_update_user_from_model(user_oauth_model, org_model['xid'])

    UserEvent('USER_LOGIN', oxid=org_model['xid'], uxid=user_model['xid'], email=user_oauth_model.email)\
        .trigger([EventService.SLACK, EventService.AUDIT, EventService.LOG])

    return_data = {
        'token': encode_user_auth_token(create_user_token_payload(user_model['xid'], org_model['xid'])),
        'meta': {
            'organization': org_model,
            'user_xid': user_model['xid'],
            'user_email': user_oauth_model.email,  # TODO: should not need this .. We should remove it
        }
    }
    return return_data, None, None


def create_or_update_user(social_id, social_network, access_code, email, username, organization_xid):

    user_social = UserDepot.fetch_user_social_by_social(social_network, social_id)

    if not user_social:
        users = UserDepot.fetch_all_users(emails=[email])
        user = users[0] if users else None

        if user:
            user_model = UserDepot.fetch_user(organization_xid, user['xid'])
        else:
            CreateEntityEvent('NEW_USER', name=username, sn=social_network, socid=social_id, email=email)\
                .trigger([EventService.SLACK, EventService.NOTIFY_SYS, EventService.AUDIT])
            user_model = UserDepot.create_organization_user(organization_xid, username, email, social_network, social_id, access_code)

    else:
        user_xid = user_social['user_xid']
        social_id = user_social['social_id']
        social_network = user_social['social_network']

        user_model = UserDepot.fetch_user(organization_xid, user_xid)
        UserDepot.update_social_access_code(user_xid, social_network, social_id, access_code)

    return user_model


def create_or_update_user_from_model(user_model, organization_xid):
    social_network = user_model.social_network
    social_id = user_model.social_id
    username = user_model.username
    email = user_model.email
    access_code = user_model.access_code

    user_model = create_or_update_user(social_id, social_network, access_code, email, username, organization_xid)

    return user_model


########################################################
# Email login
########################################################

def _domain_overrides(email):

    # override for dedicated deploys
    if email in ['admin@projectskeleton.com'] and os.environ['TARGET_SUB_DOMAIN'] not in ['app', 'org']:
        domain = os.environ['EMAIL_DOMAINS'].split(',')[0]
        return domain

    if email in ['admin_01@projectskeleton.com']:
        domain = "google.com"
        return domain

    if email in ['admin_02@projectskeleton.com']:
        domain = "amazon.com"

        return domain

    return None


def _validate_email(email):
    sections = email.split('@')
    if len(sections) == 2:
        if os.environ['TARGET_SUB_DOMAIN'] in ['app']:
            domain = 'system_public'

        elif os.environ['TARGET_SUB_DOMAIN'] in ['org']:
            domain = _domain_overrides(email)
            if not domain:
                domain = sections[1]
                if domain in ['gmail.com', 'outlook.com', 'yahoo.com']:
                    return False, domain

        else:
            domain = _domain_overrides(email)
            if domain not in os.environ['EMAIL_DOMAINS'].split(','):
                PreCreateEvent('TARGET_MISMATCH', domain=domain, email=email, target=os.environ['TARGET_SUB_DOMAIN']) \
                    .trigger([EventService.SLACK, EventService.NOTIFY_SYS])
                return False, domain
            if not domain:
                domain = sections[1]
                if domain in ['gmail.com', 'outlook.com', 'yahoo.com']:
                    return False, domain

        return True, domain
    return False, None


def validate_email_and_send_login_code(email):
    valid, domain = _validate_email(email)

    if not valid:
        SystemEvent('INVALID_EMAIL_LOGIN_DETECTED', email=email).trigger([EventService.SLACK, EventService.LOG])
        return False

    org_model = OrganizationDepot.fetch_by_domain(domain)
    if not org_model:
        name = domain.split('.com')[0].capitalize()
        org_model = OrganizationDepot.create_organization(name, domain)

    login_code_data = UserEmailLoginDepot.create_login_code(org_model['xid'], email)

    login_code = login_code_data['login_code']
    send_email_login_code(email, login_code)

    SystemEvent('EMAIL_INVITE_SEND', email=email, code=login_code).trigger([EventService.SLACK])

    return True


def validate_invite_code(email, entered_code):
    valid, domain = _validate_email(email)

    org_model = OrganizationDepot.fetch_by_domain(domain)

    if not org_model:
        return None, Reason.ORGANIZATION_NOT_REGISTERED, None

    login_code_data = UserEmailLoginDepot.select_login_code(org_model['xid'], email)
    login_code = login_code_data['login_code']

    if entered_code != login_code:
        return None, Reason.INVITE_CODE_INVALID, None

    system_user_oauth_model = UserOAuthModel(None, 'system_email_login', email, email, email, email, domain=domain)
    payload, reason, msg = fetch_user_auth_token(system_user_oauth_model)
    # send_email_login_successful(email)

    return payload, reason, msg


########################################################
# Ghost
########################################################


def fetch_is_admin(organization_xid, admin_xid):
    is_admin = is_user_admin(organization_xid, admin_xid)
    return is_admin


def fetch_all_system_users_for_admin(organization_xid, admin_xid):
    if not is_user_admin(organization_xid, admin_xid):
        return False, None

    users = UserDepot.fetch_all_users()

    from collections import defaultdict
    grouped_users = defaultdict(list)
    for user in users:
        grouped_users[user['organization_xid']].append({'xid': user['xid'], 'email': user['email']})
    return True, grouped_users


def ghost_user(organization_xid, admin_user_xid, ghost_user_xid):

    is_admin = is_user_admin(organization_xid, admin_user_xid)
    if not is_admin:
        return None, Reason.GHOSTING_FAILED, 'Ghosting not allowed for this user'

    # organization_xid is admin_user_xid's org .. not ghost_user_xid's org!! .. hence passing in None
    user_model = UserDepot.fetch_user(None, ghost_user_xid)

    if os.environ['TARGET_SUB_DOMAIN'] in ['app']:
        domain = 'system_public'
    elif os.environ['TARGET_SUB_DOMAIN'] in ['org']:
        domain = user_model['email'].split('@')[1]
    else:
        domain = user_model['email'].split('@')[1]

    org_model = OrganizationDepot.fetch_by_domain(domain)

    return_data = {
        'token': encode_user_auth_token(create_user_token_payload(user_model['xid'], org_model['xid'])),
        'meta': {
            'organization': org_model,
            'user_xid': user_model['xid'],
        }
    }
    return return_data, None, None


def fetch_user(organization_xid, user_xid):

    user_info = fetch_basic_info(organization_xid, user_xid)

    data = {
        'info': user_info,
    }
    return data


def fetch_basic_info(organization_xid, user_xid):
    from datetime import datetime

    user = UserDepot.fetch_full_user(organization_xid, user_xid)
    joined_ts = int(user['user']['inserted_at'])
    joined_on = datetime.utcfromtimestamp(joined_ts / 1000).strftime('%b %Y')

    avatar = "https://ui-avatars.com/api/?name={}".format(user['user']['username'])
    if user['user_social']:
        for user_social in user['user_social']:
            if 'avatar' in user_social:
                avatar = user_social['avatar']
                break

    data = {
        'name': user['user']['username'],
        'img_src': avatar,
        'joined_date': joined_on,
    }
    return data
