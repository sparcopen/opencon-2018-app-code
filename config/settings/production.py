from config.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['.opencon2018.org'] # production domain
SECRET_KEY = os.environ.get('SECRET_KEY')

# 2017-07-01`16:41:59 -- moved from common settings file
SEND_EMAILS = True
