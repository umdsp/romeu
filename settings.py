# Django settings for ctda project.
import os
import sys

gettext = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Kevin Zurawel', 'hello@arborwebsolutions.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ctda',                      # Or path to database file if using sqlite3.
        'USER': 'ctdauser',                      # Not used with sqlite3.
        'PASSWORD': 'b0@rdwalk',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
# adding the apps directory to the first position of the PYTHON_PATH, but keeping our dir in the top too
sys.path.insert(0, os.path.join(PROJECT_PATH, ''))

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detroit'

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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/ctda/www/html/media/'

STATICFILES_DIRS = (
	'/ctda/www/html/static',
)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://ctda.miami.edu/media/'

STATIC_URL = 'http://ctda.miami.edu/static/'

STATIC_ROOT = '/ctda/www/html/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://ctda.miami.edu/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'w#sjwc#ov(g*a)_b+sa31raerncoi7@5pt@algjc0@9^soqrc*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

INTERNAL_IPS = ('127.0.0.1', '129.171.249.144', '10.221.14.57', '10.179.1.200',)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/ctda/django/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'sorl.thumbnail',
    'reversion',
    'archive',
    'workflow',
    'modeltranslation',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'debug_toolbar',
    'ajax_select',
    'selectable',
    'smart_selects',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    'rosetta',
    'taggit',
    'tinymce',
    'haystack',
    'south',
)

# Modeltranslation settings
LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
)
MODELTRANSLATION_TRANSLATION_REGISTRY = 'archive.translation'

AJAX_LOOKUP_CHANNELS = {
    'creator': ('archive.lookups', 'CreatorLookup'),
    'production': ('archive.lookups', 'ProductionLookup'),
    'festival': dict(model='archive.FestivalOccurrence', search_field='title'),
    'location': ('archive.lookups', 'LocationLookup'),
    'workrecord': ('archive.lookups', 'WorkRecordLookup'),
    'role': ('archive.lookups', 'RoleLookup')
}

# Django debug toolbar settings
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
    'SHOW_TEMPLATE_CONTEXT': False,
}

DEFAULT_LANG = "en"

HAYSTACK_SITECONF = 'archive.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = '/ctda/django/django_whoosh_index'
HAYSTACK_INCLUDE_SPELLING = False