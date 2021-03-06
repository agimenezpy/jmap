# Django settings for jma project.
import os
JMA_ADMIN_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Alberto G.', 'albergimenez@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'asuncion'             # Or path to database file if using sqlite3.
DATABASE_USER = 'gisadm'             # Not used with sqlite3.
DATABASE_PASSWORD = 'ge0spatial'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Asuncion'
DEFAULT_CHARSET='ISO-8859-1'
FILE_CHARSET="ISO-8859-1"
SESSION_ENGINE = "django.contrib.sessions.backends.file"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-py'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i8=-4wat+b=-dn@pxoz&4a*gk7awa^4!i&^@%48lr0ce9&+j1r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'web.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(JMA_ADMIN_DIR, 'templates'),
    '/usr/share/python-support/python-django/django/contrib/gis/templates/',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.sites',
    'web.geo',
    'web.tiles'
)

GOOGLE_MAPS_API_KEY = "ABQIAAAA2EhgZ1jVWk36csfuDTqSMRScZ9FFBPdIfs42p3375FIhFRQUIxRyAlTKkDfq3zQh_52s_D1M7jY22w&amp;hl=es"

BASE_URL = "http://localhost"
ROOT_PROJECT_FOLDER = "/home/agimenez/Desktop/ProyectoWeb/jmawiki/jma/cartografia/"
DISK_CACHE = "/tmp"
MAPFILE_ROOT = ROOT_PROJECT_FOLDER
MAPNIK_MAPFILE = MAPFILE_ROOT + '/asuncion.xml'
TILE_DIR = "/home/agimenez/Desktop/ProyectoWeb/jmawiki/public/masu/"
TILE_MAPFILE = MAPFILE_ROOT + '/masuncion.xml'