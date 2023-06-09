import os
from typing import Optional

from celery import Celery


setting_module: Optional[str] = os.environ.get("DJANGO_SETTINGS_MODULE")
if not setting_module:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketeer.settings.develop')
    
app = Celery('ticketeer')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()