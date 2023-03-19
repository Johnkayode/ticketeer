"""
WSGI config for ticketeer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from typing import Optional

from django.core.wsgi import get_wsgi_application

setting_module: Optional[str] = os.environ.get("DJANGO_SETTINGS_MODULE")
if not setting_module:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketeer.settings.develop')

application = get_wsgi_application()
