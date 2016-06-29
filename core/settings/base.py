# -*- coding: utf-8 -*-
import os


class Config(object):
    '''
    Base configuration class. Subclasses should include configurations for
    testing, development and production environments

    '''

    DEBUG = True
    ASSETS_DEBUG = False  # not DEBUG

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_ECHO = False

    # Mail settings
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    DEFAULT_MAIL_CHANNEL = ''
    MAIL_DEFAULT_SENDER = ''
    MAIL_SUPPRESS_SEND = True
    MAIL_FAIL_SILENTLY = False

    UPLOADS_DEFAULT_DEST = os.path.join(
        os.path.dirname(os.path.abspath(__name__)), 'uploads')

    PROTOCOL = 'http://'

    # Admin configurations
    ADMIN_USERNAME = ''
    ADMIN_PASSWORD = ''
    ADMIN_EMAIL = ''
    ADMIN_FULL_NAME = ''

    # Celery configurations
    CELERY_BROKER_URL = 'amqp://guest@localhost//'
    CELERY_TIMEZONE = 'Africa/Lagos'

    LOGFILE_NAME = ''
    LOGIN_VIEW = 'main.index'

    DOMAIN = 'localhost:8000'

    # AWS configurations. Replace this with the defaults for your environment.
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    S3_BUCKET_NAME = ''

    FLASK_ASSETS_USE_S3 = False
    USE_S3 = True

    USE_S3_DEBUG = False

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Elastic Search configurations
    ES_CONFIG = [
        {'host': 'localhost'}
    ]
    ES_INDEX = ''
