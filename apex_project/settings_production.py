import os
from pathlib import Path

# Import base settings
from .settings import *  # noqa: F401,F403

# SECURITY
DEBUG = False

# Allowed hosts – will be set via environment variable or default to localhost
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')

# Secret key from environment
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Ensure WhiteNoise is used (already in MIDDLEWARE)

# Media files – persistent storage location
MEDIA_ROOT = BASE_DIR / 'media'

# Secure cookie settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', 'True') == 'True'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Database configuration – use DATABASE_URL if provided, else fallback to PostgreSQL defaults
if os.getenv('DATABASE_URL'):
    # Use dj-database-url to parse the URL (ensure package installed)
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(os.getenv('DATABASE_URL'))
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'apexdb'),
        'USER': os.getenv('POSTGRES_USER', 'apexuser'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'apexpass'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }

# Logging – simple console logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
