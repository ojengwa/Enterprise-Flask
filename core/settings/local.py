# -*- coding: utf-8 -*-
import os
from core.settings.base import Config


class DevConfig(Config):
    ''' Configuration class for site development environment '''

    DOMAIN = 'locahost:5000'
    SQLALCHEMY_DATABASE_URI = ''
    DATABASE = SQLALCHEMY_DATABASE_URI
    SETUP_DIR = os.path.join(os.path.dirname(
        os.path.abspath(__name__)), 'setup')

    MAX_RETRY_COUNT = 3
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    DEFAULT_MAIL_CHANNEL = ''
    MAIL_DEFAULT_SENDER = ''

    # Sample Mailgun Config
    MAILGUN_API_USERNAME = ''
    MAILGUN_API_KEY = ''
    MAILGUN_API_URL = ''
    MAILGUN_DOMAIN = ''
    MAILGUN_MESSAGES_URL = '%s/%s/messages' % (MAILGUN_API_URL, MAILGUN_DOMAIN)
