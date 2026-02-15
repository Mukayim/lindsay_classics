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
# LOAD .env FROM PROJECT ROOT (only locally)
# ────────────────────────────────────────────────
env_path = ROOT_DIR / '.env'

# We only attempt to load dotenv if the file exists
# (Railway/production does not have .env files)
dotenv_loaded = False

if env_path.is_file():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        dotenv_loaded = True
        print(f"[Django] Loaded .env from: {env_path}")
    except ImportError:
        print("[Django] Warning: python-dotenv not installed → skipping .env loading")
    except Exception as e:
        print(f"[Django] Error loading .env: {e}")
else:
    print("[Django] No .env file found at {env_path} → using system environment variables")

# ────────────────────────────────────────────────
# SECURITY & DEBUG
# ────────────────────────────────────────────────
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError(
        "DJANGO_SECRET_KEY environment variable is not set.\n"
        "→ Local: add it to .env file in project root\n"
        "→ Production: add it in Railway → Variables tab"
    )

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [
    '.railway.app',
    'localhost',
    '127.0.0.1',
    'lindsay.up.railway.app',
    # 'your-custom-domain.com',  # ← add when you have one
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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ────────────────────────────────────────────────
# URLS & TEMPLATES - UPDATED FOR REACT
# ────────────────────────────────────────────────
ROOT_URLCONF = 'backend.urls'

# Add React build directory to templates
REACT_BUILD_DIR = ROOT_DIR / 'frontend' / 'dist'
TEMPLATES_DIRS = [os.path.join(BASE_DIR, 'templates')]

# If React build exists, add it to template dirs
if REACT_BUILD_DIR.exists():
    TEMPLATES_DIRS.append(str(REACT_BUILD_DIR))
    print(f"[Django] React build found at: {REACT_BUILD_DIR}")
else:
    print(f"[Django] Warning: React build directory not found at {REACT_BUILD_DIR}")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,  # Now includes both templates/ and frontend/dist/
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
# DATABASE – conditional SSL only for Postgres
# ────────────────────────────────────────────────
db_url = os.getenv('DATABASE_URL')

if db_url and 'postgres' in db_url.lower():
    # Railway Postgres → enable SSL
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    # Local SQLite or other non-Postgres DB → no SSL
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url or 'sqlite:///db.sqlite3',
            conn_max_age=0,
        )
    }

# ────────────────────────────────────────────────
# CORS – relaxed in dev, restricted in prod
# ────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://lindsay.up.railway.app",
    # "https://your-custom-domain.com",  # ← add later
]
CORS_ALLOW_CREDENTIALS = True

# ────────────────────────────────────────────────
# STATIC & MEDIA FILES (Whitenoise + React)
# ────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = ROOT_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files directories - include React assets
STATICFILES_DIRS = []

# Add React assets if they exist
if REACT_BUILD_DIR.exists():
    REACT_ASSETS_DIR = REACT_BUILD_DIR / 'assets'
    if REACT_ASSETS_DIR.exists():
        STATICFILES_DIRS.append(str(REACT_ASSETS_DIR))
        print(f"[Django] React assets found at: {REACT_ASSETS_DIR}")

# Add any other static directories
OTHER_STATIC_DIR = BASE_DIR / 'static'
if OTHER_STATIC_DIR.exists():
    STATICFILES_DIRS.append(str(OTHER_STATIC_DIR))

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
# SECURITY & HTTPS (Railway already enforces HTTPS)
# ────────────────────────────────────────────────
if not DEBUG:
    # IMPORTANT: Do NOT enable SECURE_SSL_REDIRECT → causes infinite loop on Railway
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
TIME_ZONE = 'Africa/Lusaka'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging – makes debugging easier in Railway
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
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}