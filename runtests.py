#!/usr/bin/env python

import sys
from os import path
from os.path import dirname, abspath

from django.conf import settings, global_settings
from nose.plugins.plugintest import run_buffered as run

if not settings.configured:
    # Configure your project here
    print "Configuring settings..."
    print "Looking for sqlite3 file in %s" % dirname(abspath(__file__))
    print dirname(abspath(__file__))
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '%s/db_data.sql'%dirname(abspath(__file__)),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
    }
    
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django_pm',

        ],
        DEBUG=True,
        SITE_ID=1,
        DATABASE_ENGINE='sqlite3',
        DATABASE_NAME='db_data.sql',
        DATABASES=DATABASES,
    )

def runtests():
    # Add app's source directory to sys.path
    parent_dir = dirname(abspath(__file__))
    sys.path.insert(0, parent_dir)

    # Run tests with whatever argument was passed to the script
    run(argv=sys.argv)

if __name__ == '__main__':
    runtests()
