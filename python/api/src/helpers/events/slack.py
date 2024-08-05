import os
import requests
import json


from flask import current_app

from .constants import EventBucket

icon_map = {

    # ADMIN_ACTION
    'GHOSTING_USER': ':ghost:',

    # PRE ORG
    'ORGANIZATION_UNTARGETED': ':red_circle:',
    'ORGANIZATION_NOT_FOUND': ':red_circle:',
    'ORGANIZATION_NOT_REGISTERED': ':red_circle:',
    'TARGET_MISMATCH': ':red_circle:',

    # POST ORG
    'LOGIN_BLOCKED': ':no_entry_sign:',
    'ORGANIZATION_PILOT_COMPLETE': ':no_entry_sign:',
    'ORGANIZATION_STOP': ':no_entry_sign:',
    'USER_PILOT_COMPLETE': ':no_entry_sign:',

    # CRITICAL_EVENT
    'USER_LOGIN': ':nerd_face:',
    'NEW_ORGANIZATION': ':rocket:',
    'NEW_USER': ':boom:',

    # USER_ACTION

    # SYSTEM_ACTION
    'EMAIL_INVITE_SEND': ':envelope_with_arrow:',
    'INVALID_EMAIL_LOGIN_DETECTED': ':envelope_with_arrow:',
}


def notify(event_bucket, event_topic, event_text, meta_dict):
    if current_app.config.get("CONST_DISABLE_EVENT_SLACK", True):
        return False

    try:
        return _notify(event_bucket, event_topic, event_text, meta_dict)
    except Exception as e:
        current_app.logger.error("EVENT_NOTIFICATION_FAIL : {}".format('----START----'))
        current_app.logger.error("EVENT_NOTIFICATION_FAIL EXCEPTION: {}".format(e))
        current_app.logger.error("EVENT_NOTIFICATION_FAIL : {}".format(event_bucket))
        current_app.logger.error("EVENT_NOTIFICATION_FAIL : {}".format(event_topic))
        current_app.logger.error("EVENT_NOTIFICATION_FAIL : {}".format(event_text))
        current_app.logger.error("EVENT_NOTIFICATION_FAIL : {}".format(meta_dict))
        current_app.logger.error("EVENT_NOTIFICATION_FAIL : {}".format('-----END-----'))


def _notify(event_bucket, event_topic, event_text, meta_dict):
    # https://api.slack.com/apps/ATCUJD6JJ/incoming-webhooks?
    channel_url_var_config = {
        # EventBucket.: "SLACK_POST_CHANNEL_URL_INFRA",
        EventBucket.ERROR: "SLACK_POST_CHANNEL_URL_UX",
        EventBucket.CRITICAL: "SLACK_POST_CHANNEL_URL_UX",
        EventBucket.WARNING: "SLACK_POST_CHANNEL_URL_USAGE",
        EventBucket.INFO: "SLACK_POST_CHANNEL_URL_USAGE",
        EventBucket.DEBUG: "SLACK_POST_CHANNEL_URL_DEBUG",
    }.get(event_bucket, "SLACK_POST_CHANNEL_URL_DEBUG")
    channel_url = current_app.config.get(channel_url_var_config)

    if not channel_url:
        return False

    meta_msg_list = [" - {}: {} ".format(k, v) for k, v in meta_dict.items()]
    meta_msg = "\n".join(meta_msg_list)
    icon = icon_map.get(event_text, ':NO_ICON_SET:')

    payload = {"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":{}: - {} {} *{}*\n```{}```".format(os.environ['TARGET_SUB_DOMAIN'], event_topic, icon, event_text, meta_msg),
        }
    }]}
    resp = requests.post(channel_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

    if resp.status_code != 200:
        current_app.logger.error("SLACK POST FAILED: {}".format(resp.text))
        return False

    return True
