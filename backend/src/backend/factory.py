from dotenv import load_dotenv
from flask import Flask


load_dotenv()


def create_app(**config_overrides):
	app = Flask(__name__, static_url_path='/static')
    
	# env config
	app.config.from_pyfile("settings.py")
    
	# config obj
	from .config import Config
	app.config.from_object(Config)
    
	# config overrides
	app.config.update(config_overrides)
    
	# sqlalchemy
	from .models.models import db
	db.init_app(app)
	
    # register blueprints
	from .blueprints.admin.views import admin
	app.register_blueprint(admin)
	from .blueprints.public.views import public
	app.register_blueprint(public)
	from .blueprints.vendor.views import vendor
	app.register_blueprint(vendor)

	# create database tables
	# with app.app_context():
		# db.drop_all()
		# db.create_all()

	# launch that sucker to the moon	
	return app