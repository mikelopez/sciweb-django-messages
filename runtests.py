#!/usr/bin/env python

import sys
from os.path import dirname, abspath

from django.conf import settings, global_settings

from nose.plugins.plugintest import run_buffered as run

if not settings.configured:
    # Configure your project here
    settings.configure(
        INSTALLED_APPS=[
            'django_pm',
        ],
        DEBUG=False,
        SITE_ID=1,
    )

def runtests():
    # Add app's source directory to sys.path
    parent_dir = dirname(abspath(__file__))
    sys.path.insert(0, parent_dir)

    # Run tests with whatever argument was passed to the script
    run(argv=sys.argv)

if __name__ == '__main__':
    runtests()
