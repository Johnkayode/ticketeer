from uuid import UUID
from celery import shared_task, Task
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from apps.tickets.models import EventTicket


@shared_task(bind=True, name="apps.tickets.tasks.generate_pdf_and_send_ticket_to_mail")
def generate_pdf_and_send_ticket_to_mail(self: Task, ticket_uid: UUID):

    event_ticket: EventTicket = get_object_or_404(EventTicket, uid=ticket_uid)
    _subject: str = "Ticket"
    _sender: str = "hello@ticketeer.io"
    _recipients: list = [event_ticket.email]
    _template: str = "tickets/mail.html"

    event_ticket.generate_qrcode()
    event_ticket.generate_ticket_pdf()

    context = {"instance": event_ticket}
    _message = get_template(_template).render(context)

    mail = EmailMessage(
        subject=_subject,
        body=_message,
        from_email=_sender,
        to=_recipients,
        reply_to=[_sender],
    )
    
    mail.attach(f"ticket.pdf", event_ticket.pdf.file.read(), "application/pdf")
    mail.content_subtype = "html"

    return mail.send()
    