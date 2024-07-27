from quart import Quart


def create_app(**config_overrides):
	app = Quart(__name__, static_url_path='/static')

	# env config
	# app.config.from_pyfile("settings.py")

	# config obj
	from .config import Config
	app.config.from_object(Config)

	# config overrides
	app.config.update(config_overrides)

	# extensions	
	from .extensions import db
	db.init_app(app)

	# register blueprints
	from .blueprints.admin.views import admin
	app.register_blueprint(admin)
	from .blueprints.public.views import public
	app.register_blueprint(public)
	from .blueprints.vendor.views import vendor
	app.register_blueprint(vendor)

	return app
