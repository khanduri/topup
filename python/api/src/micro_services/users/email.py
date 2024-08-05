import os
from datetime import datetime

from src.helpers.emails import send_email
from src.helpers.constants import get_app_constant


def send_email_login_code(email, login_code):
    system_host = get_app_constant('SERVER_HOST', 'https://app.{}.com')
    app_name = 'APP_NAME'

    subject = 'Email login code for {}'.format(email)
    login_link = "{}/login/email".format(system_host)
    content = """
    <table cellspacing="0" cellpadding="0" border="0" width="600" class="content-table" style="padding: 10px 32px; border-bottom: 1px solid #EEEEEE;">
        <tr>
            <td style="font-size: 14px; line-height: 20px; padding: 5px 0; color: #454545;">
                Your login code is: <b><i style=" color: #333333;">{}</i></b>
            </td>
        </tr>
        <tr>
            <td style="font-size: 14px; line-height: 20px; padding: 5px 0; color: #454545;">
                Please use this code to login into <a href="{}">{}</a>!
            </td>
        </tr>
        <tr>
            <td style="font-size: 12px; font-style: italic; line-height: 20px; color: #757575; padding: 15px 0;">
                Login Meta:

                <table cellspacing="0" cellpadding="0" border="0" width="600" class="content-table">
                    <tr>
                        <td style="font-size: 10px; padding: 0 25px; color: #757575">
                            E-Mail: {}
                        </td>
                    </tr>
                    <tr>
                        <td style="font-size: 10px; padding: 0 25px; color: #757575">
                            Trigger time (UTC): {}
                        </td>
                    </tr>
                </table>

            </td>
        </tr>
    </table>
    """.format(login_code, login_link, app_name, email, datetime.utcnow())

    sent = send_email(subject, content, email)
    return sent


def send_email_login_successful(email):
    app_name = 'APP_NAME'

    subject = 'Successful email login for {}'.format(email)
    login_link = "https://{}.APP_NAME_HOST.com".format(os.environ['TARGET_SUB_DOMAIN'])
    content = """
    <div>
        <span>Login was successful to your <a href="{}">{}</a> account!</span>
        <br />
        <br />
        <strong>Login Meta:</strong>
        <br />
        <span>E-Mail: {}</span>
    </div>
    """.format(login_link, app_name, email)

    return send_email(subject, content, email)
