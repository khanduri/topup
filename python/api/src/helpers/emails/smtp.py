import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from flask import current_app

from .constants import HTML_SKELETON
from src import company_configs as cc


########################################################################################
# SMTP
# https://support.google.com/a/answer/176600?hl=en#zippy=%2Cuse-the-gmail-smtp-server
########################################################################################
SMPT_DOMAIN = os.environ['SMPT_DOMAIN']
SMPT_PORT = os.environ['SMPT_PORT']
SMPT_ACCOUNT_EMAIL_ADDRESS = os.environ['SMPT_ACCOUNT_EMAIL_ADDRESS']
SMPT_ACCOUNT_EMAIL_PASSWORD = os.environ['SMPT_ACCOUNT_EMAIL_PASSWORD']


_server = None


def _get_email_server_conn():
    global _server
    if not _server:
        _server = smtplib.SMTP_SSL(SMPT_DOMAIN, SMPT_PORT)
        _server.login(SMPT_ACCOUNT_EMAIL_ADDRESS, SMPT_ACCOUNT_EMAIL_PASSWORD)
        # _server = smtplib.SMTP(SMPT_DOMAIN)
    return _server


def _reset_connection():
    global _server
    if _server:
        try:
            _server.quit()
        except Exception as exp:
            pass
        _server = None


def send_smtp_email(subject, content, to_list=None, cc_list=None, bcc_list=None):

    if not (to_list or cc_list or bcc_list):
        return True

    sender = SMPT_ACCOUNT_EMAIL_ADDRESS
    # sender_title = "{} | {}".format(cc.CONFIG['NAME']['PRODUCT'], cc.CONFIG['NAME']['COMPANY'])
    sender_title = "{} team".format(cc.CONFIG['NAME']['PRODUCT'])

    message = MIMEText(HTML_SKELETON.format(content), 'html')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = formataddr((str(Header(sender_title, 'utf-8')), sender))
    if to_list:
        message['To'] = ", ".join(to_list)
    if cc_list:
        message['CC'] = ", ".join(cc_list)
    if bcc_list:
        message['BCC'] = ", ".join(bcc_list)

    email_retries = 2
    email_sent = False
    email_list = []
    if to_list:
        email_list += to_list
    if cc_list:
        email_list += cc_list
    if bcc_list:
        email_list += bcc_list

    while email_retries > 0 and not email_sent:
        try:
            server = _get_email_server_conn()
            server.sendmail(sender, email_list, message.as_string())
            email_sent = True

        except Exception as exp:
            _reset_connection()
            email_retries = email_retries - 1
            current_app.logger.warning("Email ERROR: email_retries: {}".format(exp))

    if not email_sent:
        current_app.logger.error("Email ERROR: Unable to send email to: {}".format(message))
        current_app.logger.warning("Email ERROR: Email list: {}".format(email_list))

    return email_sent
