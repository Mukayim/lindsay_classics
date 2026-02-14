# backend/settings.py
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# ────────────────────────────────────────────────
# BASE PATHS
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent  # project root (where frontend/ and backend/ live)

# Load .env from project root (Railway ignores .env but good for local)
env_path = ROOT_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)

# ────────────────────────────────────────────────
# SECURITY & DEBUG
# ────────────────────────────────────────────────
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is not set")

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['.railway.app', 'localhost', '127.0.0.1']
# Railway auto-adds your custom domain(s) — no need to hardcode them

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
    'users',  # your custom user app
    'shop',   # assuming this is your main app
]

AUTH_USER_MODEL = 'users.User'

# ────────────────────────────────────────────────
# MIDDLEWARE
# ────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',           # must be near top
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',     # after security, before others
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
        'DIRS': [ROOT_DIR / 'frontend' / 'dist'],  # React build output
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
# DATABASE – RAILWAY MAGIC
# ────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,           # keep connections alive longer
        conn_health_checks=True,    # recommended for Railway/Neon
        ssl_require=True,           # Railway Postgres requires SSL
    )
}

# Fallback for local dev (SQLite or local Postgres)
if not os.getenv('DATABASE_URL'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

# ────────────────────────────────────────────────
# CORS – Relaxed for dev, strict in prod
# ────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = DEBUG  # ← only allow all in development!
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Add your production frontend domain(s) here when deployed
]

CORS_ALLOW_CREDENTIALS = True

# ────────────────────────────────────────────────
# STATIC & MEDIA FILES (Whitenoise + React build)
# ────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collected files go here

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# React build folder (Vite / Create React App output)
REACT_BUILD_DIR = ROOT_DIR / 'frontend' / 'dist'
if REACT_BUILD_DIR.exists():
    STATICFILES_DIRS = [REACT_BUILD_DIR]
else:
    STATICFILES_DIRS = []

# Serve React index.html for all non-API routes (SPA routing)
# Add this to urls.py if not already done:
# from django.views.generic import TemplateView
# urlpatterns += [path('', TemplateView.as_view(template_name='index.html'))]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ────────────────────────────────────────────────
# REST FRAMEWORK
# ────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # ← change to IsAuthenticated in prod!
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# ────────────────────────────────────────────────
# SECURITY & HTTPS (Railway enforces HTTPS)
# ────────────────────────────────────────────────
if not DEBUG:
    SECURE_SSL_REDIRECT = True              # Railway handles redirect, but good to have
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000          # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ────────────────────────────────────────────────
# OTHER SETTINGS
# ────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka'  # Zambia time – Kitwe/Copperbelt
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging (useful on Railway)
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