"""
Django settings for TaggedNews project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_URL = '/static/thumbnails/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'siteModel','static','media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wh!2(en#%yy_*!+ty^t)*naams--12cdve)r%*b0%vj!lwvf64'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['.fuagra.kz']
LOGIN_URL = "/login/"

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'notifications',
    'siteModel',
	# 'oauth2_provider',
 #    'corsheaders',
    'simple_email_confirmation',
	
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# 'corsheaders.middleware.CorsMiddleware',
 #    'oauth2_provider.middleware.OAuth2TokenMiddleware',
)

ugettext = lambda s: s

LANGUAGES = (
    ('kk', ugettext('Kazakh')),
    ('ru', ugettext('Russian')),
    ('en', ugettext('English')),
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'oauth2_provider.backends.OAuth2Backend',
    
)

ROOT_URLCONF = 'TaggedNews.urls'

WSGI_APPLICATION = 'TaggedNews.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'test_db',
        'NAME': 'taggednews_db',
        'USER': 'taggednews',
        'PASSWORD': 'taggednews',
    }
}

REST_FRAMEWORK = {
    'PAGINATE_BY_PARAM': 'page_size',
    'PAGINATE_BY': 60, # old val 40; original 20
}

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '1.0',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': '',
    'is_authenticated': True,
    'is_superuser': True,
    'permission_denied_handler': None,
    'info': {
        'description': 'API for TaggedNews website.',
        'title': 'TaggedNews API',
    },
    'doc_expansion': 'none',
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'siteModel.User'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'support@fuagra.kz'
EMAIL_HOST_PASSWORD = 'KKGAASayat'
EMAIL_PORT = 587

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
