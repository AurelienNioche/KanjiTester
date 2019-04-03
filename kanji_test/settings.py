# -*- coding: utf-8 -*-
# 
#  settings.py
#  kanji_test
#  
#  Created by Lars Yencken on 2008-06-13.
#  Copyright 2008-06-13 Lars Yencken. All rights reserved.
# 

"""Django settings for kanji_test project."""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!d*%m--x1di4wn#^7$z89-sayp22ik#szexlz^+de_4!l99@e^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'kanji_test.tutor',
    'kanji_test.lexicon',
    'kanji_test.drill',
    # 'kanji_test.util',
    'kanji_test.user_model',
    # 'kanji_test.plugins.visual_similarity',
    # 'kanji_test.plugins.reading_alt',
    # 'kanji_test.plugins.reading_alt.hierarchy',
    'kanji_test.user_profile',
    # 'kanji_test.analysis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'registration'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'kanji_test.middleware.TagLanguageMiddleware',
]

ROOT_URLCONF = 'kanji_test.urls'

# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kanji_test.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'KanjiTester',
            'USER': 'admin',
            'PASSWORD': 'password',
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

PROJECT_NAME = 'Kanji Tester'

# from os import path
#
# PROJECT_NAME = 'Kanji Tester'
#
# DEBUG = True
# TEMPLATE_DEBUG = DEBUG
#
# ADMINS = (
#     # ('Your Name', 'your_email@domain.com'),
# )
#
# MANAGERS = ADMINS
#
# DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
# DATABASE_NAME = ''             # Or path to database file if using sqlite3.
# DATABASE_USER = ''             # Not used with sqlite3.
# DATABASE_PASSWORD = ''         # Not used with sqlite3.
# DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
# DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Location of any additional resources
DATA_DIR = ''
#
# # Local time zone for this installation. Choices can be found here:
# # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# # although not all choices may be available on all operating systems.
# # If running in a Windows environment this must be set to the same as your
# # system time zone.
# TIME_ZONE = 'Australia/Melbourne'
#
# # Language code for this installation. All choices can be found here:
# # http://www.i18nguy.com/unicode/language-identifiers.html
# LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# # If you set this to False, Django will make some optimizations so as not
# # to load the internationalization machinery.
# USE_I18N = True

# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#
# # Absolute path to the directory that holds static.
# # Example: "/home/static/static.lawrence.com/"
# MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')
#
# # URL that handles the static served from MEDIA_ROOT. Make sure to use a
# # trailing slash if there is a path component (optional in other cases).
# # Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = '/static/'
#
# # URL prefix for admin static -- CSS, JavaScript and images. Make sure to use a
# # trailing slash.
# # Examples: "http://foo.com/media/", "/static/".
# ADMIN_MEDIA_PREFIX = '/static/admin/'

# # Make this unique, and don't share it with anybody.
# SECRET_KEY = 'dc6hz00zcf8wym4hsx0jf-%c)_hq%n)rt55@*!(*3y9^48pj-s'
#
# # List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.load_template_source',
#     'django.template.loaders.app_directories.load_template_source',
# #     'django.template.loaders.eggs.load_template_source',
# )

# MIDDLEWARE_CLASSES = (
#     'django.middleware.gzip.GZipMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.middleware.doc.XViewMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'kanji_test.middleware.TagLanguageMiddleware',
# )

# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.core.context_processors.auth',
#     'django.core.context_processors.debug',
#     'django.core.context_processors.i18n',
#     'django.contrib.messages.context_processors.messages',
#     'kanji_test.context_processors.basic_vars',
# )

# ROOT_URLCONF = 'kanji_test.urls'

# TEMPLATE_DIRS = (
#     os.path.join(PROJECT_ROOT, 'templates'),
# )
#
# FIXTURE_DIRS = (
#     os.path.join(PROJECT_ROOT, 'fixtures'),
# )

# INSTALLED_APPS = (
#     'django.contrib.auth',
#     'django.contrib.admin',
#     'django.contrib.contenttypes',
#     'django.contrib.humanize',
#     'django.contrib.messages',
#     'django.contrib.sessions',
#     'django.contrib.sites',
#     'kanji_test.tutor',
#     'kanji_test.lexicon',
#     'kanji_test.drill',
#     'kanji_test.util',
#     'kanji_test.user_model',
#     'kanji_test.plugins.visual_similarity',
#     'kanji_test.plugins.reading_alt',
#     'kanji_test.plugins.reading_alt.hierarchy',
#     'kanji_test.user_profile',
#     'kanji_test.analysis',
#     'checksum',
#     'registration',
#     'south',
# )

TEST_DATABASE_CHARSET = 'utf8'
TEST_DATABASE_COLLATION = 'utf8_general_ci'

CONTROL_DRILL_PLUGINS = (
    'kanji_test.plugins.basic_drills.ReadingQuestionFactory',
    'kanji_test.plugins.basic_drills.SurfaceQuestionFactory',
    'kanji_test.plugins.basic_drills.GlossQuestionFactory',
)

ADAPTIVE_DRILL_PLUGINS = (
    'kanji_test.plugins.reading_alt.ReadingAlternationQuestions',
    'kanji_test.plugins.basic_drills.GlossQuestionFactory',
    'kanji_test.plugins.visual_similarity.VisualSimilarityDrills',
)

DRILL_PLUGINS = list(set(CONTROL_DRILL_PLUGINS + ADAPTIVE_DRILL_PLUGINS))

USER_MODEL_PLUGINS = (
    'kanji_test.plugins.visual_similarity.VisualSimilarity',
    'kanji_test.plugins.reading_alt.KanjiReadingModel',
)

# auth
AUTH_PROFILE_MODULE = 'user_profile.userprofile'

# drill; drill_plugins
N_DISTRACTORS = 5
QUESTIONS_PER_SET = 10
QUESTIONS_PER_PAGE = 5

# visual_similarity
MIN_TOTAL_DISTRACTORS = 15
MAX_GRAPH_DEGREE = MIN_TOTAL_DISTRACTORS

# reading_alt
ALTERNATION_ALPHA = 0.5
VOWEL_LENGTH_ALPHA = 0.05
PALATALIZATION_ALPHA = 0.05
MAX_READING_LENGTH = 30
UTF8_BYTES_PER_CHAR = 3 # For cjk chars

# registration
ACCOUNT_ACTIVATION_DAYS = 15

N_ROWS_PER_INSERT = 10000
DEFAULT_LANGUAGE_CODE = 'eng'
UPDATE_EPSILON = 0.2

# When True, enables the debugging static view.
DEPLOYED = False

DEFAULT_FROM_EMAIL = 'Kanji Tester <kanjitester@gakusha.info>'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kanjitester@gakusha.info'
EMAIL_HOST_PASSWORD = 'Rulgoittee'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

GOOGLE_ANALYTICS_CODE = None

# Overwrite any of these settings with local customizations.
try:
    from local_settings import *
except ImportError:
    pass
