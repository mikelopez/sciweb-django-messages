#!/usr/bin/env python

import sys
import os

from django.conf import settings, global_settings

if not settings.configured:

    # Configure your project here
    DATABASE_ENGINE = 'django.db.backends.sqlite3',
    DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'db_data.sql')
    DATABASES = {
            "default": {
                'ENGINE': DATABASE_ENGINE,
                'NAME': DATABASE_NAME,
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
    }
    settings.configure(
        #DATABASE_ENGINE = DATABASE_ENGINE,
        #DATABASE_NAME = DATABASE_NAME,
        DATABASES = DATABASES,
        INSTALLED_APPS = ('django.contrib.auth',
                          'django.contrib.contenttypes',
                          'django.contrib.sessions',
                          'django.contrib.admin',
                          'django_pm',),
        DEBUG=False,
        SITE_ID=1,
    )

from django.test.simple import run_tests
def runtests():
    # Add app's source directory to sys.path
    failures = run_tests(['django_pm',], verbosity=1)
    if failures:
        sys.exit(failures)
    """
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent_dir)

    # Run tests with whatever argument was passed to the script
    run(argv=sys.argv)"""

if __name__ == '__main__':
    runtests()
