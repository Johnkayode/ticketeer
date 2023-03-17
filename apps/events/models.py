from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel



class Event(BaseModel):
    # organizer (user)
    # co-ordinators (user)
    name = models.CharField(_("name"), max_length=150)
    from_date = models.DateTimeField(_("from_date"))
    to_date = models.DateTimeField(_("to_date"))
    description = models.TextField(null=True, blank=True)
    venue = models.TextField(null=True, blank=True)
    max_participants = models.PositiveIntegerField(default=2)

    #is_expired = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    

    @property
    def is_expired(self):
        if self.to_date is None:
            return False
        return self.to_date < timezone.now()
