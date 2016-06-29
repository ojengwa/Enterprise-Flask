# -*- coding: utf-8 -*-
from core.settings.local import DevConfig


class ProdConfig(DevConfig):
    ''' Configuration class for site production environment '''

    DOMAIN = ''
    SERVER_NAME = None
    DEBUG = False
    TEST = False
    SQLALCHEMY_ECHO = False

    LOGIN_VIEW = 'main.index'

    # Configuring sentry logging
    SENTRY_DSN = ''
    SENTRY_INCLUDE_PATHS = []
    SENTRY_USER_ATTRS = []
