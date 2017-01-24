# Django settings for med project.



DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
AUTH_PROFILE_MODULE = 'common.UserProfile'
HTTPS_SUPPORT = True
#SESSION_COOKIE_SECURE = True

import os

import dj_database_url


DATABASES = {'default': dj_database_url.config()}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': '',                      # Or path to database file if using sqlite3.
#        'USER': '',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Novosibirsk'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = ')nhz2jc4ewa5sb%q*mi9k$)z+vx)z82e4!5(&vdgto1t_-#f#4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'common.middleware.SecureRequiredMiddleware',
    # 'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

SETTINGS_PATH = os.path.normpath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    # os.path.join(os.path.dirname(__file__), 'medint/html'),
    # os.path.join(SETTINGS_PATH, 'medint/templates'),
    # os.path.join(os.path.dirname(__file__), 'medint/tags_html'),
    # os.path.join(os.path.dirname(__file__), 'medint/tags_html'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.request',
  'django.contrib.auth.context_processors.auth',
)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

#STATICFILES_DIRS = (
#    os.path.join(os.path.dirname(__file__), 'static'),
#)

INSTALLED_APPS = (

    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'common',
    'medint',
    'wiki',
    'staff',
    'messaging',
    'gunicorn',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #  'django.contrib.admindocs',
    'south',

)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'user'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = 'password'

NOTIFICATION_EMAIL = 'mac@medicalintelligence.com'
FEEDBACK_EMAIL = 'librett@medicalintelligence.com'



ADMIN_MEDIA_PREFIX = '/static/admin/'
LOGIN_URL = '/login'

if os.environ.get('CIRCLECI'):
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'circle_test',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '0.0.0.0',
        'PORT': '5432',
    }
}

AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'


SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https',)

AUTH_USER_MODEL = 'common.MedintUser'

AUTHENTICATION_BACKENDS = (
    'common.backends.YubiBackend',
)

INDIVO_SERVER_PARAMS = {"api_base": "http://ec2-1-1-1-1.compute-1.amazonaws.com:8081",
                 "authorization_base": "http://ec2-1-1-1-1.compute-1.amazonaws.com:8081"}

INDIVO_CONSUMER_PARAMS = {"consumer_key": "chrome", "consumer_secret": "chrome"}
INDIVO_USER_EMAIL = "indivo@user.email"




if os.environ.get('TYPE'):
    if 'STAGING' == os.environ.get('TYPE'):
        from config.staging import *
    elif 'PRODUCTION' == os.environ.get('TYPE'):
        from config.production import *
else:
    if os.environ.get('CIRCLECI'):
        from config.staging import *
    else:
        from config.local_settings import *
