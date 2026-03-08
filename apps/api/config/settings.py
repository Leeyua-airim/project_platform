# apps/api/config/settings.py
from pathlib import Path
from dotenv import load_dotenv  

import os

BASE_DIR = Path(__file__).resolve().parent.parent
# apps/api/.env 파일 로딩
load_dotenv(BASE_DIR / ".env") 

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY is not set")

DJANGO_DEBUG = os.environ.get("DJANGO_DEBUG", "0")
DEBUG = DJANGO_DEBUG == "1"

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# 로컬 기본값은 localhost Redis, Render에서는 REDIS_URL을 환경변수로 주입하면 그대로 사용 가능.
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Seoul"

DJANGO_DEBUG = os.environ.get("DJANGO_DEBUG", "0")
DEBUG = DJANGO_DEBUG == "1"

ALLOWED_HOSTS = ["project-platform-81bi.onrender.com", 
                 ".onrender.com", 
                 "127.0.0.1",
                 "localhost",]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'core',
    'users',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # React(vite) 개발 서버 허용
]

MIDDLEWARE = [
    # 'core.middleware.CORSMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DRF 기본 인증/권한 설정
# 모든 API 요청은 기본적으로 Supabase JWT 인증을 거치도록 설정
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "common.authentication.SupabaseJWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# Supabase 프로젝트 URL
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")

# Supabase가 공개하는 JWKS 주소
# Django는 이 주소의 공개키로 access token 서명을 검증함
SUPABASE_JWKS_URL = os.environ.get(
    "SUPABASE_JWKS_URL",
    f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json" if SUPABASE_URL else "",
)

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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
