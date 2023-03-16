from django.db import models


class BaseManager(models.Manager):
  def __init__(self, *args, **kwargs):
    super(BaseManager, self).__init__(*args, **kwargs)

  def get_queryset(self):
    return super().get_queryset().filter(deleted_at__isnull=True, is_deleted=False)