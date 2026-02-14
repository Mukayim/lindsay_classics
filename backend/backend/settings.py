# backend/settings.py
import os
from pathlib import Path
import dj_database_url

# ────────────────────────────────────────────────
# BASE PATHS
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent          # backend/backend/
ROOT_DIR = BASE_DIR.parent                          # project root (lindsay/)

# ────────────────────────────────────────────────
# SECURITY & DEBUG
# ────────────────────────────────────────────────
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is not set")

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['.railway.app', 'localhost', '127.0.0.1', 'lindsay.up.railway.app']
# Railway auto-adds domains — this covers your current URL

# ────────────────────────────────────────────────
# APPLICATIONS
# ────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'users',   # custom user app
    'shop',    # main app
]

AUTH_USER_MODEL = 'users.User'

# ────────────────────────────────────────────────
# MIDDLEWARE
# ────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',           # must be near top
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',      # serves static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ────────────────────────────────────────────────
# URLS & TEMPLATES
# ────────────────────────────────────────────────
ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ROOT_DIR / 'frontend' / 'dist'],  # React/Vite build output
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

WSGI_APPLICATION = 'backend.wsgi.application'

# ────────────────────────────────────────────────
# DATABASE – RAILWAY POSTGRES
# ────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,           # required for Railway/Neon Postgres
    )
}

# Local fallback (only used when no DATABASE_URL)
if not os.getenv('DATABASE_URL'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

# ────────────────────────────────────────────────
# CORS – Secure in production
# ────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = DEBUG  # only open in dev
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://lindsay.up.railway.app",          # your Railway frontend URL
    # Add your custom domain later, e.g. "https://www.lindsayclassics.com"
]
CORS_ALLOW_CREDENTIALS = True

# ────────────────────────────────────────────────
# STATIC & MEDIA FILES (Whitenoise + React build)
# ────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = ROOT_DIR / 'staticfiles'              # collect to project root level

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# React build folder
REACT_BUILD_DIR = ROOT_DIR / 'frontend' / 'dist'
if REACT_BUILD_DIR.exists():
    STATICFILES_DIRS = [REACT_BUILD_DIR]
else:
    STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ────────────────────────────────────────────────
# REST FRAMEWORK
# ────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # change to IsAuthenticated in prod!
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# ────────────────────────────────────────────────
# SECURITY & HTTPS (Railway enforces HTTPS – do NOT redirect again!)
# ────────────────────────────────────────────────
if not DEBUG:
    # SECURE_SSL_REDIRECT = False          # ← disabled to fix redirect loop
    # Railway handles HTTP → HTTPS automatically
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000          # 1 year HSTS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ────────────────────────────────────────────────
# OTHER SETTINGS
# ────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka'  # Zambia time
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging (visible in Railway logs)
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