# -*- coding: utf-8 -*-
# 
#  settings.py
#  kanji_tester
#  
#  Created by Lars Yencken on 2008-06-13.
#  Copyright 2008-06-13 Lars Yencken. All rights reserved.
# 

"""Django settings for kanji_tester project."""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!d*%m--x1di4wn#^7$z89-sayp22ik#szexlz^+de_4!l99@e^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    u'127.0.0.1'
]


# Application definition

INSTALLED_APPS = [
    'analysis',
    'checksum',
    'tutor',
    'lexicon',
    'drill',
    'util',
    'user_model',
    'user_profile',
    'plugins.visual_similarity',
    'plugins.reading_alt.hierarchy',
    'plugins.reading_alt',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'kanji_tester.middleware.TagLanguageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'kanji_tester.urls'

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

WSGI_APPLICATION = 'kanji_tester.wsgi.application'


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

# Location of any additional resources
DATA_DIR = 'data'

os.environ['CJKDATA'] = os.path.join(DATA_DIR, 'cjkdata')

CONTROL_DRILL_PLUGINS = (
    'plugins.basic_drills.ReadingQuestionFactory',
    'plugins.basic_drills.SurfaceQuestionFactory',
    'plugins.basic_drills.GlossQuestionFactory',
)

ADAPTIVE_DRILL_PLUGINS = (
    'plugins.reading_alt.reading_alt.ReadingAlternationQuestions',
    'plugins.basic_drills.GlossQuestionFactory',
    'plugins.visual_similarity.visual_similarity.VisualSimilarityDrills',
)

DRILL_PLUGINS = list(set(CONTROL_DRILL_PLUGINS + ADAPTIVE_DRILL_PLUGINS))

USER_MODEL_PLUGINS = (
    'plugins.visual_similarity.visual_similarity.VisualSimilarity',
    'plugins.reading_alt.reading_alt.KanjiReadingModel',
)

# auth
AUTH_PROFILE_MODULE = 'user_profile.UserProfile'

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
UTF8_BYTES_PER_CHAR = 3  # For cjk chars

# registration
ACCOUNT_ACTIVATION_DAYS = 15

N_ROWS_PER_INSERT = 10000
DEFAULT_LANGUAGE_CODE = 'eng'
UPDATE_EPSILON = 0.2

# When True, enables the debugging static view.
DEPLOYED = False

DEFAULT_FROM_EMAIL = 'Kanji Tester <username@gmail.com>'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'username@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# GOOGLE_ANALYTICS_CODE = None

# Overwrite any of these settings with local customizations.
try:
    from kanji_tester.local_settings import *
except ImportError:
    print("No local settings has been defined. Mail sending will crash.")
