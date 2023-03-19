from .base import *


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

