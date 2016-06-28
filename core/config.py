
import os
from celery.schedules import crontab

class Config(object):
	"""
	Base configuration class. Subclasses should include configurations for
	testing, development and production environments

	"""

	DEBUG = True
	SECRET_KEY = '\x91c~\xc0-\xe3\'f\xe19PE\x93\xe8\x91`uu"\xd0\xb6\x01/\x0c\xed\\\xbd]H\x99k\xf8'
	SQLALCHEMY_ECHO = False
	# Mail settings
	MAIL_SERVER = 'smtp.mailgun.org'
	MAIL_PORT = 587
	MAIL_USERNAME = "postmaster@myfitted.mailgun.org"
	MAIL_PASSWORD = "myfitted"
	DEFAULT_MAIL_CHANNEL = "mailgun"
	MAIL_DEFAULT_SENDER = 'daemon@fitted.com'
	MAIL_SUPPRESS_SEND = True
	MAIL_FAIL_SILENTLY = False
	UPLOADS_DEFAULT_DEST = os.path.join(os.path.dirname(os.path.abspath(__name__)), "uploads")
	CLOUDFILES_USERNAME = "emotub"
	CLOUDFILES_API_KEY = "80a129ef023b8027f4ba4523786feacf"

	PROTOCOL = "http://"

	ADMIN_USERNAME = "fitted"
	ADMIN_PASSWORD = "fitted"
	ADMIN_EMAIL = "admin@fitted.com"
	ADMIN_FULL_NAME = "fitted Admin"

	RESTRICTED_DOMAINS = ["admin", "preview", "www", "www1", "www2", "http", "https", "mail", "api", "docs",
			"shop", "m", "mobile", "facebook", "twitter", "google", "linkedin", "instagram"]

	ASSETS_DEBUG = False # not DEBUG


	CELERY_BROKER_URL = "amqp://guest@localhost//"

	CELERY_TIMEZONE = 'Africa/Lagos'

	LOGFILE_NAME = 'fitted'

	LOGIN_VIEW = 'main.index'

	DOMAIN = "fitted.dev:2500"

	AWS_ACCESS_KEY_ID = 'AKIAIQEGDMORT3P4F7DA'

	AWS_SECRET_ACCESS_KEY = "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"

	S3_BUCKET_NAME = "fitted"

	FLASK_ASSETS_USE_S3 = False

	USE_S3 = True

	USE_S3_DEBUG = False

	DEBUG_TB_INTERCEPT_REDIRECTS = False

	ES_CONFIG = [
		{"host": "localhost"}
	]

	ES_INDEX = "fitted"

	TWILIO_API_SID = "AC3813535560204085626521",
	TWILIO_API_TOKEN = "2flnf5tdp7so0lmfdu3d7wod"

	FACEBOOK = dict(
		base_url='https://graph.facebook.com/',
		request_token_url=None,
		access_token_url='/oauth/access_token',
		authorize_url='https://www.facebook.com/dialog/oauth',
		consumer_key="1557243561175841", 
		consumer_secret="d716ba47b8c530b370682ce079d490d8",
		request_token_params={'scope':'email, public_profile, user_friends'}
	)


# Configuration classes for fitted sites

class DevConfig(Config):
	""" Configuration class for site development environment """

	DOMAIN = "api.fitted.dev:5000"
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/fitted'
	DATABASE = SQLALCHEMY_DATABASE_URI
	SETUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'setup')
	MAX_RETRY_COUNT = 3
	MAIL_SERVER = 'smtp.mailgun.org'
	MAIL_PORT = 587
	MAIL_USERNAME = "postmaster@my500shops.mailgun.org"
	MAIL_PASSWORD = "my500shops"
	DEFAULT_MAIL_CHANNEL = "mailgun"
	MAIL_DEFAULT_SENDER = 'daemon@500shops.com'
	MAILGUN_API_USERNAME = "api"
	MAILGUN_API_KEY = "key-15y6uvsrwkm4pcdkxwdsv56ci5-13b-3"
	MAILGUN_API_URL = "https://api.mailgun.net/v2"
	MAILGUN_DOMAIN = "my500shops.mailgun.org"
	MAILGUN_MESSAGES_URL = "%s/%s/messages" % (MAILGUN_API_URL, MAILGUN_DOMAIN)
	# MAILGUN_API_USERNAME = "api"
	# MAILGUN_API_KEY = "key-15y6uvsrwkm4pcdkxwdsv56ci5-13b-3"
	# MAILGUN_API_URL = "https://api.mailgun.net/v2"
	# MAILGUN_DOMAIN = "myfitted.mailgun.org"
	# MAILGUN_MESSAGES_URL = "%s/%s/messages" % (MAILGUN_API_URL, MAILGUN_DOMAIN)
	

	FACEBOOK = dict(
		base_url='https://graph.facebook.com/',
		request_token_url=None,
		access_token_url='/oauth/access_token',
		authorize_url='https://www.facebook.com/dialog/oauth',
		consumer_key="1557243561175841", 
		consumer_secret="d716ba47b8c530b370682ce079d490d8",
		request_token_params={'scope':'email,public_profile, user_friends'}
	)


class TestConfig(DevConfig):
	""" Configuration class for site testing environment """

	# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/fitted_test'
	SQLALCHEMY_DATABASE_URI = 'sqlite://'
	TEST = True
	SQLALCHEMY_ECHO = False


class ProdConfig(DevConfig):
	""" Configuration class for site testing environment """

	DOMAIN = "fitted.com"
	SERVER_NAME = None
	DEBUG = False
	TEST = False
	SQLALCHEMY_ECHO = False

	LOGIN_VIEW = 'main.index'

	# Configuring sentry logging
	SENTRY_DSN = "http://d2793cd20be84b32a0f0af8e3750e8de:6e86677a4645400d9e1a7575aaa5d94b@sentry.blustair.com/4"
	SENTRY_INCLUDE_PATHS = ['fitted']
	SENTRY_USER_ATTRS = ['username', 'full_name', 'email']