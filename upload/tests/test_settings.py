import os

APP_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))

DEBUG = True
THUMBNAIL_DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'upload.db',
    }
}
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = APP_ROOT + STATIC_URL
MEDIA_ROOT = STATIC_ROOT + 'media/'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/',  # back to homepage after profile pic GFK test
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(APP_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'upload.tests.test_urls'
INSTALLED_APPS = (
    'upload',
    'django.contrib.staticfiles',

    # auth (for user uploaded collections)
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
)
THUMBNAIL_ALIASES = {
    '': {
        'large':  {'size': (400, 400), 'crop': True},
        'medium': {'size': (180, 180), 'crop': True},
        'small':  {'size': (100, 100), 'crop': True},
        'tiny':   {'size': (50, 50),   'crop': True},
    },
}
SECRET_KEY = 'foobar'
