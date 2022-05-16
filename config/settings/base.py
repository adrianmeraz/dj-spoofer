import os
import logging.config

import environ

env = environ.Env()
environ.Env.read_env(env_file='.env')

SECRET_KEY = env('SECRET_KEY')

LOGLEVEL = env('LOGLEVEL').upper()

LOGGING_CFG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
        'verbose': {
            'format': '[{levelname}/{processName} {threadName}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOGLEVEL,
            'propagate': True,
        },
        'django': {
            'level': LOGLEVEL,
            'handlers': ['console'],
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'environ': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
        'faker': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'hpack': {
            'handlers': ['console'],
            'level': LOGLEVEL,
            'propagate': False,
        },
    },
}
logging.config.dictConfig(LOGGING_CFG)

db_from_env = env.db_url()
db_from_env.update({
    'CONN_MAX_AGE': 600,
})

DATABASES = {
    'default': db_from_env,
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SITE_ID = 1

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djstarter',
    'djspoofer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = 'djstarter.AuthUser'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ]
        },
    }
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

KEYLOG_FILENAME = env.get_value('KEYLOG_FILENAME', default=None)
SSL_VERIFY = env.bool('SSL_VERIFY')
PROXY_URL = env.get_value('PROXY_URL', default=None)
PROXY_USERNAME = env('PROXY_USERNAME')
PROXY_PASSWORD = env('PROXY_PASSWORD')

PROXYRACK_COUNTRY_WEIGHTS = [
    ('US', .70),
    ('CA', .12),
    ('UK', .12),
    ('AU', .06),
]

H2_FINGERPRINT_API_BASE_URL = 'https://mediasploit.com'
HOWSMYSSL_API_BASE_URL = 'https://www.howsmyssl.com'
INCOLUMITAS_API_BASE_URL = 'https://api.incolumitas.com'
INCOLUMITAS_TCPIP_API_BASE_URL = 'https://tcpip.incolumitas.com'
INCOLUMITAS_TLS_API_BASE_URL = 'https://tls.incolumitas.com'
INTOLI_API_BASE_URL = 'https://raw.githubusercontent.com'
PROXYRACK_API_BASE_URL = 'http://api.proxyrack.net'
