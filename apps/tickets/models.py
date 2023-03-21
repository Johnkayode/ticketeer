from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files import File
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from apps.events.models import Event
from apps.tickets.utils import generate_ticket_reference
from base.models import BaseModel

from io import BytesIO
from typing import Optional
from weasyprint import HTML
import qrcode


class EventTicket(BaseModel):
    _qrcode_directory_path = "tickets/qrcode"
    _pdf_directory_path = "tickets/pdf"


    reference = models.CharField(max_length=100, unique=True, default=generate_ticket_reference)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("name"), max_length=150)
    email = models.EmailField(_("email"))
    qrcode = models.ImageField(_("qr code"), upload_to=_qrcode_directory_path)
    pdf = models.FileField(upload_to=_pdf_directory_path, null=True, blank=True)
    is_expired = models.BooleanField(default=False)


    @classmethod
    def verify_ticket(cls, data: str, event: Event) -> Optional["EventTicket"]:
        """ Verify ticket """
        data = data.split("_")
        try:
            _ticket = cls.objects.get(
                event=event,
                uid=data[0], 
                reference=data[1], 
                is_expired=False
            )
            _ticket.is_expired = True
            _ticket.save(update_fields=["is_expired"])
            return _ticket, "Ticket verified successfully"
        except cls.DoesNotExist:
            # TODO: log error
            return None, "Ticket does not exist or has expired."
        except Exception as err:
            # TODO: log error
            return None, err

    def generate_qrcode(self) -> None:
        """ generate qrcode using reference and uid """
        _data = "".join([str(self.uid), "_", self.reference])
        _qr_code = qrcode.make(_data)

        _file_name = f'{self.reference}.png'
        _stream = BytesIO()
        _qr_code.save(_stream, 'PNG')
        # reread the file for cloudinary
        _stream.seek(0)
        self.qrcode.save(_file_name, File(_stream), save=True)

    def generate_ticket_pdf(self) -> None:
        """ generate ticket pdf and attach qrcode """
        template = "tickets/pdf.html"
        context = {"instance": self}
        html_string = render_to_string(template, context)
        _file = HTML(string=html_string).write_pdf()
        _file_name = f"{self.reference}.pdf"
        self.pdf.save(_file_name, ContentFile(_file))
