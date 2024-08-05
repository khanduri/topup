from flask import current_app

from src.depot.audit import AuditDepot


def record(event_bucket, event_topic, event_text, meta_dict):
    if current_app.config.get("CONST_DISABLE_EVENT_AUDIT", True):
        return False

    try:
        AuditDepot.insert_log(event_bucket, event_topic, event_text, meta_dict)
    except Exception as e:
        current_app.logger.error("EVENT_AUDIT_FAIL : {}".format('----START----'))
        current_app.logger.error("EVENT_AUDIT_FAIL EXCEPTION: {}".format(e))
        current_app.logger.error("EVENT_AUDIT_FAIL : {}".format(event_bucket))
        current_app.logger.error("EVENT_AUDIT_FAIL : {}".format(event_topic))
        current_app.logger.error("EVENT_AUDIT_FAIL : {}".format(event_text))
        current_app.logger.error("EVENT_AUDIT_FAIL : {}".format(meta_dict))
        current_app.logger.error("EVENT_AUDIT_FAIL : {}".format('-----END-----'))
