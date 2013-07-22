###############################################################
# File Paths
###############################################################
import os, sys

PROJECT_DIR = os.path.dirname(__file__)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR + '/templates',
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

sys.path.append(os.path.dirname(PROJECT_DIR))
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.join(PROJECT_DIR, 'apps'))
sys.path.append(os.path.join(PROJECT_DIR, 'libs'))

SCHOOL_URL = "school.edu"


###############################################################
# Basic Logging Setup
###############################################################
import logging

LOG_DATE_FORMAT = '%d %b %Y %H:%M:%S'
LOG_FORMATTER = logging.Formatter(
    u'%(asctime)s | %(levelname)-7s | %(name)s | %(message)s',
    datefmt=LOG_DATE_FORMAT)

CONSOLE_HANDLER = logging.StreamHandler() # defaults to stderr
CONSOLE_HANDLER.setFormatter(LOG_FORMATTER)
CONSOLE_HANDLER.setLevel(logging.DEBUG)


###############################################################
# Django Server Setup
###############################################################

ADMINS = (
# ('Admin', 'admin@admin.com'),

)

INTERNAL_IPS = (
#'127.0.0.1',
)

MANAGERS = ADMINS

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.contrib.messages.context_processors.messages',
    "django.core.context_processors.request",
    "datamining.apps.profiles.context_processors.template_settings",
    "datamining.apps.profiles.context_processors.recent_updates",
    "datamining.apps.profiles.context_processors.school_url",
    # "grappelli.context_processors.admin_template_path",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
    'datamining.middleware.threadlocals.ThreadLocals',
    #'datamining.middleware.sslredirect.SSLRedirect', # Uncomment if you want the site running under SSL
    'django.middleware.csrf.CsrfViewMiddleware',
    'axes.middleware.FailedLoginMiddleware',
)

MAINTENANCE_IGNORE_URLS = [
    r'^/media/.*',
    r'^/admin/.*',
    r'^/accounts/.*'
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_extensions',
    'django.contrib.markup',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'grappelli',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.comments',
    'haystack',
    'tagging',
    'sorl.thumbnail',
    'basic.blog',
    'basic.inlines',
    'basic.tools',
    'datamining.apps.profiles',
    'datamining.apps.cv',
    'datamining.apps.importer',
    'datamining.apps.api',
    'datamining.apps.reporting',
    'datamining.apps.mobile',
    'south',
    'objectpermissions',
    'piston',
    'feedjack',
    'ajax_select',
    'ajax_filtered_fields',
    'social_bookmarking',
    'djangocalais',
    'axes',
    #'permissions',
    'password_required',
)


###############################################################
# Password Required Settings
###############################################################
# currently used to pw protect CEA exports /api/faculty
PASSWORD_REQUIRED_PASSWORD = ''

###############################################################
# Django Axes
###############################################################
AXES_COOLOFF_TIME = 24
AXES_LOCKOUT_TEMPLATE = PROJECT_DIR + '/templates/401.html'


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_URL = '/media/'


###############################################################
# Web Server Paths
###############################################################                                
ROOT_URLCONF = 'datamining.urls'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'
ADMIN_TOOLS_MEDIA_URL = '/media/'
ADMIN_TOOLS_MENU = 'datamining.menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'datamining.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'datamining.dashboard.CustomAppIndexDashboard'

#set up the autocomplete channels for admin and forms, etc.
AJAX_LOOKUP_CHANNELS = {
    'person': ('profiles.lookups', 'PersonLookup'),
    'course': ('profiles.lookups', 'CourseLookup'),
    'committee': ('reporting.lookups', 'CommitteeLookup'),
    'department': ('profiles.lookups', 'DepartmentLookup'),
    'school': ('profiles.lookups', 'SchoolLookup'),
    'division': ('profiles.lookups', 'DivisionLookup'),
    'program': ('profiles.lookups', 'ProgramLookup'),
    'group': ('profiles.lookups', 'GroupLookup'),
    'work': ('profiles.lookups', 'WorkLookup'),
    'semester': dict(model='profiles.semester', search_field='term'),
    'user': dict(model='auth.user', search_field='username'),
    'project': dict(model='profiles.project', search_field='title'),
    'expertise': dict(model='profiles.expertise', search_field='name'),
    'worktype': dict(model='profiles.worktype', search_field='name'),
}

SSL_URLS = (
    r'^/$',
    r'^/admin/',
    r'.*/edit/$',
    r'.*/add/$',
    r'^/ajax_select/',
    r'^/accounts/',
    r'^/logout/$',
    r'^grantperm$',
    r'^viewperm$',
    r'^changeperm/\d+$',
    r'^editperm/\d+$',
    r'^deleteperm/',
    r'^/media/',
)

SECURE_LOGIN = True


###############################################################
# for django-ajax-selects (for autocomplete mainly)
# this instructs that module to inline include some necessary js
# could also upgrade to django 1.4 and use collectstatic instead of this.
# see
#   https://github.com/crucialfelix/django-ajax-selects/blob/master/README.md
# and
#   https://github.com/crucialfelix/django-ajax-selects/issues/10
###############################################################
AJAX_SELECT_INLINES = 'inline'


# Configure settings locally, overriding defaults above

###############################################################
# Haystack Search Setup
# 
# (note: this must come after LOCAL_SETTINGS, which must set SOLR_ROOT
# & HAYSTACK_SOLR_URL)
###############################################################
try:
    SOLR_SCHEMA_PATH = SOLR_ROOT + 'solr/conf/schema.xml'
    SOLR_DATA_DIR = SOLR_ROOT + 'solr/data'
    HAYSTACK_SITECONF = 'datamining.apps.search_sites'
    HAYSTACK_SEARCH_ENGINE = 'solr'
except NameError:
    print "WARNING: skipping SOLR initialization"

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/'

