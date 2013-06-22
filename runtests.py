#!/usr/bin/env python

import sys
import os

from django.conf import settings, global_settings
from nose.plugins.plugintest import run_buffered as run

if not settings.configured:
    # Configure your project here
    settings.configure(
        DATABASE_ENGINE = 'sqlite3',
        DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'db_data.sql'),
        DATABASES = {"NAME": DATABASE_NAME, "ENGINE": DATABASE_ENGINE},
        INSTALLED_APPS = ('django.contrib.auth',
                          'django.contrib.contenttypes',
                          'django.contrib.sessions',
                          'django.contrib.admin',
                          'django_pm.tests',),
        DEBUG=False,
        SITE_ID=1,
    )

def runtests():
    # Add app's source directory to sys.path
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent_dir)

    # Run tests with whatever argument was passed to the script
    run(argv=sys.argv)

if __name__ == '__main__':
    runtests()
