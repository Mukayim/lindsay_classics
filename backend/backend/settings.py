# backend/settings.py
import os
from pathlib import Path
import dj_database_url

# ────────────────────────────────────────────────
# BASE PATHS
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent          # points to backend/backend/
ROOT_DIR = BASE_DIR.parent                          # points to project root (lindsay/)

# ────────────────────────────────────────────────
# LOAD .env FROM PROJECT ROOT (only locally)
# ────────────────────────────────────────────────
env_path = ROOT_DIR / '.env'

# Load .env only if the file actually exists
# (Railway / production environments do not have .env files)
if env_path.is_file():
    from dotenv import load_dotenv
    load_dotenv(env_path)
    print(f"Loaded .env from: {env_path}")   # optional - helps debugging locally
else:
    print("No .env file found → using system environment variables")

# ────────────────────────────────────────────────
# SECURITY & DEBUG
# ────────────────────────────────────────────────
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError(
        "DJANGO_SECRET_KEY environment variable is not set. "
        "Add it to .env (local) or Railway Variables (production)."
    )

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [
    '.railway.app',
    'localhost',
    '127.0.0.1',
    'lindsay.up.railway.app',
    # add custom domain later if you have one
]

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
    'users',
    'shop',
]

AUTH_USER_MODEL = 'users.User'

# ────────────────────────────────────────────────
# MIDDLEWARE
# ────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'DIRS': [ROOT_DIR / 'frontend' / 'dist'],
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
# DATABASE
# ────────────────────────────────────────────────
db_url = os.getenv('DATABASE_URL')

if db_url and 'postgres' in db_url.lower():
    # Production: Railway Postgres – enable SSL
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    # Local: SQLite or any non-Postgres DB – no SSL
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url or 'sqlite:///db.sqlite3',
            conn_max_age=0,  # no pooling for SQLite
        )
    }

# ────────────────────────────────────────────────
# CORS
# ────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://lindsay.up.railway.app",
    # "https://your-custom-domain.com" ← add later
]
CORS_ALLOW_CREDENTIALS = True

# ────────────────────────────────────────────────
# STATIC & MEDIA FILES
# ────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = ROOT_DIR / 'staticfiles'              # collectstatic target

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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
        'rest_framework.permissions.AllowAny',  # ← tighten in production!
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# ────────────────────────────────────────────────
# SECURITY & HTTPS (Railway handles HTTPS redirection)
# ────────────────────────────────────────────────
if not DEBUG:
    # Do NOT set SECURE_SSL_REDIRECT = True here — causes redirect loop on Railway
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ────────────────────────────────────────────────
# OTHER SETTINGS
# ────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging – visible in Railway logs
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