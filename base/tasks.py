from celery import shared_task, Task
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import get_template


@shared_task(bind=True, name="base.tasks.send_email")
def send_email(self: Task, subject: str, recipients: list, template: str, context: dict):

    
    _subject: str = subject
    _sender: str = "hello@ticketeer.io"
    _recipients: list = recipients
    _template: str = template


    _message = get_template(_template).render(context)

    mail = EmailMessage(
        subject=_subject,
        body=_message,
        from_email=_sender,
        to=_recipients,
        reply_to=[_sender],
    )

    mail.content_subtype = "html"

    return mail.send()
    