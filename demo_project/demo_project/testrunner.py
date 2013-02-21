__author__ = 'Marcos Lopez'
# http://github.com/mikelopez

from django.test.simple import DjangoTestSuiteRunner
import settings

class BaseAppsTestNoDb(DjangoTestSuiteRunner):
  def setup_databases(self, **kwargs):
    """ override the db stuff from DjangoTestSuiteRunner """
    pass

  def teardown_databases(self, old_config, **kwargs):
    """ override db teardown from DjangoTestSuiteRunner """
    pass

  def build_suite(self, test_labels, *args, **kwargs):
    return super(BaseAppsTestNoDb, self).build_suite(test_labels or \
        [i for i in settings.INSTALLED_APPS if not "django" in i], *args, **kwargs)
