from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.events.models import Event
from apps.tickets.utils import generate_ticket_reference
from base.models import BaseModel


class EventTicket(BaseModel):
    reference = models.CharField(max_length=100, unique=True, default=generate_ticket_reference)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("name"), max_length=150)
    email = models.EmailField(_("email"))
    qrcode = models.ImageField(_("qr code"))

