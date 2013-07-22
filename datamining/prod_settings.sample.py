from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = False
STAGE_NAME = 'PROD' # either PROD or DEV

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

###############################################################
# Database Settings
###############################################################                                       
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # You must use MySQL
        'NAME': 'datamining',                  # Or path to database file if using sqlite3.
        'USER': 'mining',                      # Not used with sqlite3.
        'PASSWORD': '',                        # Not used with sqlite3.
        'HOST': '',                            # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                            # Set to empty string for default. Not used with sqlite3.
        }
    }

###############################################################
# Search Server Settings
###############################################################             
SOLR_ROOT = '/home/mining/src/apache-solr-1.4.0/staging/'
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'

#####
# importer app settings
#####
MYSQLDUMP_CMD = '/usr/local/mysql/bin/mysqldump'
GZIP_CMD = '/usr/bin/gzip'
import os
DB_BACKUP_DIR = os.path.dirname(__file__) + '/databackups'

#####
# email settings
#####
### for staging and development or testing:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
### replace the above line with the following for the live site:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST =
# EMAIL_PORT =
# EMAIL_HOST_USER =
# EMAIL_HOST_PASSWORD =
# EMAIL_USE_TLS =

EMAIL_SUBJECT_PREFIX = '[datamyne] '


#####
# LDAP settings
#####
AUTHENTICATION_BACKENDS = (
    #'django_auth_ldap.backend.LDAPBackend',
    'datamining.apps.profiles.backends.SchoolLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_LDAP_SERVER_URI = "ldaps://"

import ldap
from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_BIND_DN = "cn=,o="
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch("o=new_school",
    ldap.SCOPE_SUBTREE, "(&(objectclass=user)(cn=%(user)s))")
AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn", "email":""}
AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_ALLOW,
}


#####
# Banner integration
#####
BANNER_IMPORT_PREFIX = ""
BANNER_IMPORT_SCRIPT = False


#####
# other misc things
#####
ADMIN_MEDIA_PREFIX = '/media/admin/'

GRAPPELLI_ADMIN_TITLE = 'DataMYNE Admin'

CALAIS_API_KEY = "your api key here"

# to disable SSL for all URLs (eg, on local dev), uncomment this line:
#SSL_URLS = ()

