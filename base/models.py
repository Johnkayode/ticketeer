from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import BaseManager

import uuid


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(_("deleted"), null=True, blank=True)
    is_deleted = models.BooleanField(null=False, default=False)

    objects = BaseManager()
    objects_with_deleted = models.Manager()

    class Meta:
        abstract = True