"""
WSGI config for opencon_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

import dotenv

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from whitenoise.django import DjangoWhiteNoise


dotenv.read_dotenv(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')))

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.developer")

# IMPORTANT: whitenoise only scans for media files upon startup, so newly added files won't be detected
# see https://github.com/evansd/whitenoise/issues/32
application = WhiteNoise(
    DjangoWhiteNoise(get_wsgi_application()),
    root=settings.MEDIA_ROOT,
    prefix=settings.MEDIA_URL,
)
