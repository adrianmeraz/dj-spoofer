from .base import *

DEBUG = True

ALLOWED_HOSTS += []

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',    # Use MD5 Hasher for faster tests - Only in DEV
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

MIGRATE = False
