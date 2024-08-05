import datetime

from flask import current_app

from src.depot.audit import AuditDepot
from src.depot.subscription import SubscriptionDepot
from src.depot.feedback import FeedbackDepot
from src.helpers.admin_auth import is_user_admin
from src.helpers.constants import get_app_constant

from src.depot.mongo.user import Organization, User, UserSocial, UserEmailLogin
from src.depot.mongo.audit import Audit


class GenericsLogic(object):

    @classmethod
    def add_feedback(cls, meta, data):
        fxid = FeedbackDepot.create_feedback(meta, data)
        return {'feedback_xid': fxid}

    @classmethod
    def fetch_feedback(cls, organization_xid, user_xid):
        is_admin = is_user_admin(organization_xid, user_xid)
        if not is_admin:
            return {}

        data = FeedbackDepot.fetch_feedbacks()
        result = {
            'is_admin': is_admin,
            'info': data,
        }
        return result

    @classmethod
    def add_subscribe(cls, email, meta, data):
        sub_xid = SubscriptionDepot.create_subscription(email, meta, data)
        return {'subscription_xid': sub_xid}

    @classmethod
    def fetch_subscribe(cls, organization_xid, user_xid):
        is_admin = is_user_admin(organization_xid, user_xid)
        if not is_admin:
            return {}

        data = SubscriptionDepot.fetch_subscription()
        result = {
            'is_admin': is_admin,
            'info': data,
        }
        return result


class MaintenanceLogic(object):

    @classmethod
    def maintenance_indexes_details(cls):

        audit_index_details = Audit.indexes_select()

        organization_index_details = Organization.indexes_select()

        user_index_details = User.indexes_select()
        user_social_index_details = UserSocial.indexes_select()
        user_email_login_index_details = UserEmailLogin.indexes_select()

        data = {
            'audit_index_details': audit_index_details,

            'organization_index_details': organization_index_details,

            'user_index_details': user_index_details,
            'user_social_index_details': user_social_index_details,
            'user_email_login_index_details': user_email_login_index_details,

        }

        return data

    @classmethod
    def maintenance_indexes_create(cls, block):

        t0 = datetime.datetime.utcnow()

        if block == '1':
            Organization.indexes_create()
            User.indexes_create()
            UserSocial.indexes_create()
            UserEmailLogin.indexes_create()
            Audit.indexes_create()

        t1 = datetime.datetime.utcnow()

        return {
            'run_seconds': (t1 - t0).seconds,
        }


class CronLogic(object):

    @classmethod
    def daily_crons(cls, context):
        data = {}

        t0 = datetime.datetime.utcnow()

        if context.get('delete_stale', {}).get('enabled', False):
            stale_data = cls.cron_delete_stale_data()
            t1 = datetime.datetime.utcnow()
            data.update({'cron_delete_stale_data': {'data': stale_data, 'run_seconds': (t1 - t0).seconds}})

        t4 = datetime.datetime.utcnow()

        return {
            'data': data,
            'run_seconds': (t4 - t0).seconds,
        }

    @classmethod
    def cron_delete_stale_data(cls):
        data = {}

        delete_days = get_app_constant('CONST_DB_EXPIRE_DAY_COUNT', 90)
        gap = datetime.timedelta(days=delete_days)
        remove_time = (datetime.datetime.utcnow() - gap).timestamp() * 1000

        stats = dict()
        # stats['cnt_TABLE'] = TABLE.delete_stale_data(remove_time)

        data.update({
            'remove_time': remove_time,
            'delete_days': delete_days,
            'stats': stats,
        })
        return data


def fetch_system_info(organization_xid, admin_xid):
    is_admin = is_user_admin(organization_xid, admin_xid)
    if not is_admin:
        return {}

    selected_keys = [
        'ENV', 'DEBUG', 'TESTING',
        'SERVER_NAME', 'TARGET_SUB_DOMAIN',
        'DEPLOY_DATE',
        'SENTRY_DNS',
    ]
    filtered = []
    selected = []
    for key in current_app.config:
        if "CONST_" in key:
            selected.append(key)
        elif "CELERY_" in key:
            selected.append(key)
        elif "CACHE_" in key:
            selected.append(key)
        elif "SLACK_" in key:
            selected.append(key)
        elif key in selected_keys:
            selected.append(key)
        else:
            filtered.append(key)

    result = {
        'is_admin': is_admin,
        'info': {
            'app_config': {key: current_app.config[key] for key in selected},
        }
    }
    return result


def fetch_system_audit_logs(organization_xid, user_xid):
    is_admin = is_user_admin(organization_xid, user_xid)
    if not is_admin:
        return {}

    audit_logs = AuditDepot.fetch_logs()
    result = {
        'is_admin': is_admin,
        'info': audit_logs,
    }
    return result
