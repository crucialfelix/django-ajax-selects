DEBUG = True
USE_TZ = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
ROOT_URLCONF = "tests.urls"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    "ajax_select",
    "tests"
]
SITE_ID = 1
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)
STATIC_URL = '/static/'
SECRET_KEY = 'inyd5fc5pymlsv@hwoc5+3_6*cm0erlxzv6i-wl0jm_kt-6rp9'

AJAX_LOOKUP_CHANNELS = {
    # tuple points to a module and class to load
    'book': ('tests.other_lookups', 'BookLookup'),
    # dict specifies an automatically constructed LookupChannel
    'author': {'model': 'tests.Author', 'search_field': 'name'},
    # unset a channel that a third-party app specified
    'user': None,
    'was-never-a-channel': None
    # LookupChannels in lookups.py are auto-loaded
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
