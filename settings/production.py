from .base import *
from dotenv import load_dotenv
import os

load_dotenv('.env_prod')  # take environment variables from .env.

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DEBUG = int(os.environ.get('DEBUG', 0))

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_prod.sqlite3',
    }
}