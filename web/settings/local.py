#!python

# -*- coding: utf-8 -*-
SECRET_KEY = 'Place your brand new security key here'
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'office2017.whistle.it',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}
PROTOCOL = 'http'
EMAIL_HOST = 'smtps.aruba.it'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'dev@risin.it'
EMAIL_HOST_PASSWORD = 'Kalimera1'
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = ['whistle']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
