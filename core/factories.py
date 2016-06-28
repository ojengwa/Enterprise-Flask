"""
factories.py

@Author: Bernard Ojengwa
@Date: October 25, 2014

This module contains application factories.
"""

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
from flask.ext.assets import Environment, Bundle
import os
from flask.ext import restful
from flask.ext.principal import Principal
from flask_mail import Mail
from flaskext.uploads import UploadSet, IMAGES, ARCHIVES, configure_uploads, \
	patch_request_class
import wtforms_json
from celery import Celery
from flask.ext.smartmigrate import Migrate
from flask_s3 import FlaskS3
from elasticsearch import Elasticsearch
from twilio.rest import TwilioRestClient
from flask_oauthlib.client import OAuth

# # new redis session management
# from flaskext.kvsession import KVSessionExtension
# import redis
# from simplekv.memory.redisstore import RedisStore

# install redis in configuration to trap errors
from raven.contrib.flask import Sentry

# Monkey patch wtforms to support json data
wtforms_json.init()


#create oauth app

oauth = OAuth()


def initialize_api(app, api):
	""" Register all resources for the API """
	api.init_app(app=app) # Initialize api first
	_resources = getattr(app, "api_registry", None)
	if _resources and isinstance(_resources, (list, tuple,)):
		for cls, args, kwargs in _resources:
			api.add_resource(cls, *args, **kwargs)



def initialize_blueprints(app, *blueprints):
	"""
	Registers a set of blueprints to an application
	"""
	for blueprint in blueprints:
		app.register_blueprint(blueprint)



def make_celery(app):
	""" Enables celery to run within the flask application context """

	celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
	celery.conf.update(app.config)
	TaskBase = celery.Task

	class ContextTask(TaskBase):
		abstract = True
		def __call__(self, *args, **kwargs):
			with app.app_context():
				return TaskBase.__call__(self, *args, **kwargs)

	celery.Task = ContextTask
	return celery



def create_app(app_name, config_obj, with_api=True):
	""" Generates and configures the main shop application. All additional """
	# Launching application
	app = Flask(app_name) # So the engine would recognize the root package

	# Load Configuration
	app.config.from_object(config_obj)

	# Loading assets
	assets = Environment(app)
	assets.from_yaml('assets.yaml')
	app.assets = assets

	# Initialize Mail
	app.mail = Mail(app)

	# Initializing login manager
	login_manager = LoginManager()
	login_manager.login_view = app.config.get('LOGIN_VIEW', 'main.index')
	# login_manager.login_message = 'You need to be logged in to access this page'
	login_manager.session_protection = 'strong'
	login_manager.setup_app(app)
	app.login_manager = login_manager

	# Initializing principal manager
	app.principal = Principal(app)

	# Initializing bcrypt password encryption
	bcrypt = Bcrypt(app)
	app.bcrypt = bcrypt

	# Initializing Database
	db = SQLAlchemy(app)
	app.db = db

	# Initializing Migrate
	migrate = Migrate(app, db, "from fitted.models import *")
	app.migrate = migrate

	photos = UploadSet('photos', IMAGES)
	archives = UploadSet('archives', ARCHIVES)

	configure_uploads(app, (photos, archives))

	patch_request_class(app, 2 * 1024 * 1024) # Patches to 2MB file uploads max.

	app.photos = photos
	app.archives = archives

	# Integrate Elasticsearch

	es_config = app.config.get("ES_CONFIG", [])

	app.es = Elasticsearch(es_config)

	# Integrate sms with Twilio
	app.sms = TwilioRestClient(app.config.get("TWILIO_API_SID"), app.config.get("TWILIO_API_TOKEN"))


	# Redis store for session management
	# The process running Flask needs write access to this directory:
	# store = RedisStore(redis.StrictRedis())

	# # this will replace the app's session handling
	# KVSessionExtension(store, app)

	# configure sentry
	# if not app.config.get("DEBUG", False):
	# 	sentry = Sentry(app)

	# 	app.sentry = sentry

	# inject celery into the app
	app.celery = make_celery(app)

	# injecting mongodb support
	# app.mongo = PyMongo(app)

	# flask s3 integration
	app.s3 = FlaskS3(app)


	# Facebook & Twitter Integration
	app.facebook = oauth.remote_app('facebook',
		app_key='FACEBOOK'
	)


	oauth.init_app(app)



	# Initializing the restful API
	if with_api:
		api = restful.Api(app, prefix='/api/v1')
		app.api = api

	# Initialize Logging
	if not app.debug:
		import logging
		from logging.handlers import RotatingFileHandler
		file_handler = RotatingFileHandler("/var/log/fitted/%s.log" % app.config.get("LOGFILE_NAME", app_name), maxBytes=500*1024)
		file_handler.setLevel(logging.WARNING)
		from logging import Formatter
		file_handler.setFormatter(Formatter(
		    '%(asctime)s %(levelname)s: %(message)s '
		    '[in %(pathname)s:%(lineno)d]'
		))
		app.logger.addHandler(file_handler)

	#include an api_registry to the application
	app.api_registry = [] #a simple list holding the values to be registered

	return app

