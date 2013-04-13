# -*- coding: utf-8 *-*
import os
import urlparse
import logging
from selenium import webdriver
# This is necessary for all installed apps to be recognized, for some reason.
os.environ['DJANGO_SETTINGS_MODULE'] = 'pumpkin.settings.test'


def before_all(context):
    # Even though DJANGO_SETTINGS_MODULE is set, this may still be
    # necessary. Or it may be simple CYA insurance.
    from django.core.management import setup_environ
    from pumpkin.settings import test as settings
    setup_environ(settings)

    ### Take a TestRunner hostage.
    from discover_runner import DiscoverRunner
    # We'll use thise later to frog-march Django through the motions
    # of setting up and tearing down the test environment, including
    # test databases.


    context.runner = DiscoverRunner(verbosity=0)


    ## If you use South for migrations, uncomment this to monkeypatch
    ## syncdb to get migrations to run.
    from south.management.commands import patch_for_test_db_setup
    patch_for_test_db_setup()

    host = context.host = 'localhost'
    port = context.port = getattr(settings, 'TESTING_SERVER_PORT', 8081)
    # NOTE: Nothing is actually listening on this port. wsgi_intercept
    # monkeypatches the networking internals to use a fake socket when
    # connecting to this port.

    from django.test.testcases import LiveServerThread

    context.server_thread = LiveServerThread(host, [port])
    context.server_thread.daemon = True
    context.server_thread.start()
    # Wait for the live server to be ready
    context.server_thread.is_ready.wait()
    if context.server_thread.error:
        raise context.server_thread.error


    def browser_url(url):
        """Create a URL for the virtual WSGI server.

        e.g context.browser_url('/'), context.browser_url(reverse('my_view'))
        """
        return urlparse.urljoin('http://%s:%d/' % (host, port), url)

    context.browser_url = browser_url

    #looger
    selenium_logger = logging.getLogger(
        'selenium.webdriver.remote.remote_connection')
    selenium_logger.setLevel(logging.WARN)
    south_logger=logging.getLogger('south')
    south_logger.setLevel(logging.WARN)




def before_scenario(context, scenario):

    # fix bug django
    from django.db import connections, DEFAULT_DB_ALIAS
    connections[DEFAULT_DB_ALIAS].settings_dict['NAME'] = 'pumpkin'

    # setUp
    context.runner.setup_test_environment()
    context.old_db_config = context.runner.setup_databases()
    context.browser = webdriver.PhantomJS()


def after_scenario(context, scenario):
    # setDown
    context.browser.quit()
    context.runner.teardown_databases(context.old_db_config)
    context.runner.teardown_test_environment()


def after_all(context):
    context.server_thread.join()

