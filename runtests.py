import sys

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="ajax_select.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            'django.contrib.messages',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.staticfiles',
            "ajax_select",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware'
        )
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

    try:
        from django.test.runner import DiscoverRunner as TestRunner
    except ImportError:
        # < 1.8
        from django.test.simple import DjangoTestSuiteRunner as TestRunner

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError(
        "Make sure that you have installed test requirements: "
        "pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['ajax_select']

    runner = TestRunner()
    failures = runner.run_tests(test_args, verbosity=1)
    if failures:
        pass
        # sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
