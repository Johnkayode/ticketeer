"""
ASGI config for ticketeer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from typing import Optional

from django.core.asgi import get_asgi_application

setting_module: Optional[str] = os.environ.get("DJANGO_SETTINGS_MODULE")
if not setting_module:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketeer.settings.develop')

application = get_asgi_application()
