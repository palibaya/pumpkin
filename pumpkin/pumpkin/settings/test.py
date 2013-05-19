from base import *

########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_ROOT = SITE_ROOT
TEST_DISCOVER_PATTERN = "test_*.py"
########### IN-MEMORY TEST DATABASE
#DATABASES = {
    #"default": {
        #"ENGINE": "django.db.backends.sqlite3",
        #"NAME": ":memory:",
        #"USER": "",
        #"PASSWORD": "",
        #"HOST": "",
        #"PORT": "",
    #},
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': normpath(join(DJANGO_ROOT, 'default.db')),
        'NAME': 'pumpkin',
        'USER': 'ata',
        'PASSWORD': 'rahasia',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}


