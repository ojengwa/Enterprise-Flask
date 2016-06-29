# -*- coding: utf-8 -*-
from core.settings.local import DevConfig


class TestConfig(DevConfig):
    """ Configuration class for site testing environment """

    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/fitted_test'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TEST = True
    SQLALCHEMY_ECHO = False
