from .smtp import send_smtp_email

from src import company_configs as cc


def send_email(subject, content, email, run_async=True):
    subject = "{}: {}".format(cc.CONFIG['NAME']['COMPANY'], subject)

    run_async = False
    if not run_async:
        # return send_sendgrid_email(subject, content, email)
        return send_smtp_email(subject, content, to_list=[email])
    else:
        from src.task.client import async_client
        task_args = (subject, content, email)
        task = async_client.send_task('task.emails.send_email_async', args=task_args)
