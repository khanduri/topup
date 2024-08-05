from .smtp import send_smtp_email

from src.helpers.task.worker import async_worker
from src.helpers.task.constants import TaskQueue


@async_worker.task(name="task.emails.send_email_async", queue=TaskQueue.SM_HIGH)
def send_email_async(subject, content, email):
    # return send_sendgrid_email(subject, content, email, send_email=send_email)
    return send_smtp_email(subject, content, to_list=[email])
