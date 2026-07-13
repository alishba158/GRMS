"""
Django settings for grms_project project.
"""

from pathlib import Path
import os
import ssl  # ✅ SSL fix ke liye

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# ===== SECURITY =====
# ============================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-oplj3t*xfjiqk+1x%f=pcoz0wtwvp9ova@#2xk8z)qxf$plz1o')

# ✅ DEBUG - Development ke liye True karein
DEBUG = True  # ✅ Change to True for development

# ✅ ALLOWED HOSTS
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

# ============================================
# ===== APPLICATION DEFINITION =====
# ============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'corsheaders',
]

LOGIN_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ============================================
# ===== MIDDLEWARE =====
# ============================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Static files serve karne ke liye
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # ✅ CSRF Middleware - Important
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'grms_project.urls'

# ============================================
# ===== TEMPLATES =====
# ============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'grms_project.wsgi.application'

# ============================================
# ===== DATABASE =====
# ============================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'grms_new'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'ssl': {'ca': '/etc/ssl/certs/ca-certificates.crt'}
        }
    }
}

# ============================================
# ===== PASSWORD VALIDATION =====
# ============================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================
# ===== INTERNATIONALIZATION =====
# ============================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================
# ===== ✅ STATIC FILES =====
# ============================================
STATIC_URL = '/static/'

# ✅ Static files ka folder (jahan aapne CSS, JS, Images rakhi hain)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# ✅ Static files collect hone ka folder (production ke liye)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✅ WhiteNoise storage (production ke liye)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================
# ===== MEDIA FILES =====
# ============================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================
# ===== DEFAULT PRIMARY KEY =====
# ============================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# ===== MESSAGES =====
# ============================================
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ============================================
# ===== CORS SETTINGS =====
# ============================================
CORS_ALLOW_ALL_ORIGINS = True

# ============================================
# ============================================
# ===== 📧 EMAIL CONFIGURATION (SMTP - REAL EMAIL) =====
# ============================================
# ============================================

# ✅ Use SMTP Backend for real emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT =465
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'fuuastislamabad1@gmail.com'
EMAIL_HOST_PASSWORD = 'kqrh glne fnbn fdeq'  # ✅ App Password
DEFAULT_FROM_EMAIL = f'GRMS System <{EMAIL_HOST_USER}>'
EMAIL_TIMEOUT = 60  # ✅ 30 se 60 kar diya

# ============================================
# ============================================
# ===== 📧 PASSWORD RESET EMAIL SETTINGS =====
# ============================================
# ============================================

# ✅ Password Reset Token Expiry (24 hours in seconds)
PASSWORD_RESET_TIMEOUT = 86400  # 24 hours

# ✅ Password Reset Email Subject
PASSWORD_RESET_SUBJECT = '🔑 Password Reset Request - GRMS'

# ============================================
# ============================================
# ===== ✅ SSL CERTIFICATE FIX =====
# ============================================
# ============================================

# ✅ SSL Certificate Verification Fix
# Disable SSL verification for development (Gmail ke liye)
ssl._create_default_https_context = ssl._create_unverified_context
print("✅ SSL verification disabled for development")