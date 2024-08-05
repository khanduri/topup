import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .constants import HTML_SKELETON

from flask import current_app

from src import company_configs as cc


########################################################################################
# SENDGRID
########################################################################################
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')


def _send_sendgrid_email(subject, content, email, send_email=True):

    # TODO: add logic to only send 3-5 times in an hour

    contact_email = cc.CONFIG['EMAIL']['PRODUCT']
    dnr_email = cc.CONFIG['EMAIL']['DNR']

    message = Mail(
        from_email='{}'.format(dnr_email),
        subject=subject,
        html_content=HTML_SKELETON.format(content)
    )
    if send_email:
        message.add_to(email)
    message.add_bcc('{}'.format(contact_email))
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        current_app.logger.error("LOGIN Email error: Unable to send email to: {}".format(message))
        return False

    return True
