# backend/settings.py
import os
from pathlib import Path
import dj_database_url

# ────────────── Paths ──────────────
BASE_DIR = Path(__file__).resolve().parent       # backend/backend/
ROOT_DIR = BASE_DIR.parent                       # project root (lindsay/)

# ────────────── Environment ──────────────
env_path = ROOT_DIR / '.env'
if env_path.is_file():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        print(f"[Django] Loaded .env from {env_path}")
    except ImportError:
        print("[Django] python-dotenv not installed → skipping .env")
    except Exception as e:
        print(f"[Django] Error loading .env: {e}")

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'super-secret')
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['*']  # Update in production

# ────────────── Installed Apps ──────────────
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

# ────────────── Middleware ──────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ────────────── URLs & Templates ──────────────
ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # React index.html
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

# ────────────── Database ──────────────
db_url = os.getenv('DATABASE_URL')
if db_url and 'postgres' in db_url.lower():
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': dj_database_url.config(default=db_url or 'sqlite:///db.sqlite3')
    }

# ────────────── CORS ──────────────
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://lindsay.up.railway.app",
]
CORS_ALLOW_CREDENTIALS = True

# ────────────── Static / Media ──────────────
STATIC_URL = '/static/'
STATIC_ROOT = ROOT_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',           # optional backend static
    BASE_DIR / 'templates',        # React build (index.html + assets)
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ────────────── REST Framework ──────────────
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# ────────────── Misc ──────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
