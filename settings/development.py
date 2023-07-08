from .base import *
import os
from dotenv import load_dotenv

load_dotenv('.env_dev')  # take environment variables from .env.

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DEBUG = int(os.environ.get('DEBUG', 0))

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_dev.sqlite3',
    }
}