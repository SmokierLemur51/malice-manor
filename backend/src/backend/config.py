import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    # SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.environ['SQLITE_DB']}.db"
    QUART_DB_DATABASE_URL = "sqlite:///src/instance/{}.db".format(os.environ["SQLITE_DB"])

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
