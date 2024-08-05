import datetime

from flask import current_app

from src.helpers.emails import send_email


def notify(event_bucket, event_topic, event_text, meta_dict):
    if current_app.config.get("CONST_DISABLE_EVENT_NOTIFY_SYS", True):
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
    email = 'prashant.khanduri@gmail.com'  # TODO: Change this email address
    subject = 'Event: {} - {}'.format(event_topic, event_text)

    meta_msg_list = [" - {}: {} ".format(k, v) for k, v in meta_dict.items()]
    meta_html = []
    for msg in meta_msg_list:
        meta_html.append('<div style="font-size: 14px; line-height: 20px; padding: 5px 0; color: #454545;">{}</div>'.format(msg))

    msg_content = "".join(meta_html)
    content = """
        <table cellspacing="0" cellpadding="0" border="0" width="600" style="padding: 10px 32px; border-bottom: 1px solid #EEEEEE;">
            <tr>
                <td style="font-size: 14px; line-height: 20px; padding: 5px 0; color: #454545;">
                    <div>
                        <div style="font-size: 18px; line-height: 20px; padding: 5px 0; color: #343434;">{}</div>
                        {}
                    </div>
                </td>
            </tr>
            <tr>
                <td style="font-size: 12px; font-style: italic; line-height: 20px; color: #757575; padding: 15px 0;">
                    Meta:
                    <table cellspacing="0" cellpadding="0" border="0" width="600">
                        <tr><td style="font-size: 10px; padding: 0 25px; color: #757575">E-Mail: {}</td></tr>
                        <tr><td style="font-size: 10px; padding: 0 25px; color: #757575">Trigger time (UTC): {}</td></tr>
                    </table>

                </td>
            </tr>
        </table>
        """.format(event_text, msg_content, email, datetime.datetime.utcnow())
    send_email(subject, content, email, run_async=True)
