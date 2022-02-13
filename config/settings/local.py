from .base import *

DEBUG = True

ALLOWED_HOSTS += [
    '0.0.0.0',
    '127.0.0.1',
    'localhost'
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',    # Use MD5 Hasher for faster tests - Only in DEV
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

MIGRATE = False
