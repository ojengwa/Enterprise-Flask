#! /usr/bin/env python

from flask.ext.script import Manager
import os
from flask.ext.assets import ManageAssets
from factories import create_app, initialize_api, initialize_blueprints
from flask.ext.smartmigrate import Migrate, MigrateCommand
import flask_s3

app = create_app('fitted', 'config.DevConfig')

logger = app.logger

# Initializing script manager
manager = Manager(app)

# Initializing Migrate
manager.add_command('db', MigrateCommand)
# #add assets command to it
manager.add_command("assets", ManageAssets(app.assets))


@manager.command
def runserver():
	""" Start the server"""

	from fitted.views.frontend import main
	
	from fitted.resources import events
	from fitted.services import authentication, products
	from fitted import api
	from fitted.subscribers import events

	# Initialize the api resources
	initialize_blueprints(app, main)
	initialize_api(app, api)


	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)


@manager.command
def runadmin():
	""" Start the server"""

	from fitted.views.admin import control
	
	from fitted.resources import assets, merchant
	from fitted.resources.admin import auth, assets
	from fitted import api

	# Initialize the api resources
	initialize_api(app, api)

	# # Import all subscriptions to initialize them
	from fitted.services import search
	from fitted.subscribers import registration, inventory, search, messages
	
	# Initialize the app blueprints
	initialize_blueprints(app, control)

	port = int(os.environ.get('PORT', 5001))
	app.run(host='0.0.0.0', port=port)



@manager.command
def syncdb(refresh=False):
	""" 
	Synchronizes (or initializes) the database
	:param refresh: drop and recreate the database
	"""
	# Apparently, we need to import the models file before this can work right.. smh @flask-sqlalchemy
	from fitted import db, models
	
	if refresh:
		logger.info("Dropping database tables")
		db.drop_all()
	logger.info("Creating database tables")
	db.create_all()
	db.session.flush()

@manager.command
def rebuild_scraper():
	"""
	Deletes and re-indexes them using the live feed from the server.
	"""

	from twisted.internet import reactor
	from scrapy.crawler import Crawler
	from scrapy import log, signals
	from scraping.spiders.konga_spider import KongaSpider
	from scrapy.utils.project import get_project_settings
	import xmltodict
	from fitted.services.search import index, delete_index

	delete_index()

	def convert_traclist(**kwargs):
		obj = dict(
			name = kwargs['ProductName'],
	        site = 'traclist',
	        category = kwargs['Category'],
	        manufacturer = kwargs['Manufacturer'],
	        sku = kwargs["ShopSKU"],
	        price = kwargs["SalePrice"],
	        url = kwargs["ProductURL"],
	        description = kwargs["ProductShortDescription"],
	        coverImage = kwargs["ImageURL"]
		)
		return obj

	x = open('pricecheck.xml').read()
	c = xmltodict.parse(x)

	offers = c['Offers']['Offer']
	for f in offers:
		obj = convert_traclist(**dict(f))
		index(**obj)

	spider = KongaSpider(domain='www.konga.com')
	settings = get_project_settings()
	crawler = Crawler(settings)
	crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
	crawler.configure()
	crawler.crawl(spider)
	crawler.start()
	log.start()
	reactor.run()


@manager.command
def install_assets():
	""" Installs all required assets to begin with """
	from startup import start
	start()



@manager.command
def upload_to_s3():
	""" Uploads static assets to Amazon s3 """
	logger.info("Starting static files uploads ")
	flask_s3.create_all(app)
	logger.info("Static files upload complete")


@manager.command
def rebuild_index():
	from fitted.services import search

	logger.info("Rebuilding search index, this might take a while. Please wait...")
	search.rebuild_index()
	logger.info("Done")



if __name__ == "__main__":
	manager.run()

