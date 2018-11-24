import string
import random

from config.settings.base import *


SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50))
)

INSTALLED_APPS += [
    'debug_toolbar',
]

# 2017-06-14`16:47:54 -- load django_extensions (runserver_plus, shell_plus)
INSTALLED_APPS += ('django_extensions', )

ALLOWED_HOSTS = ['applytest.opencon2018.org', 'localhost'] # test domain

# 2017-07-01`16:41:46 -- moved from common settings
SEND_EMAILS = False
