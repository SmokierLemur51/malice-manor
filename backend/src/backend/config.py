import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.environ['SQLITE_DB']}.db"
    """ PG database conn
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:5432/{}".format(
            os.environ["DB_USERNAME"],
            os.environ['DB_PASSWORD'],
            os.environ['DB_HOST'],
            os.environ['DATABASE_NAME'],
        )
    """

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
