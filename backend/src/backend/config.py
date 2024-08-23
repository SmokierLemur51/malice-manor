import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    
    # Generate key with secrets.token_urlsafe()
    SECRET_KEY = 'this-really-needs-to-be-changed'
    # Generate good salt for password with secrets.SystemRandom().getrandbits(128)
    # SECURITY_PASSWORD_SALT = os.environ["SECURITY_PASSWORD_SALT"]

    # Have session and remember cookie be samesite (flask/flask_login)
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict"

    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.environ['SQLITE_DB']}.db"
    # PG database conn
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:5432/{}".format(
    #        os.environ["DB_USERNAME"],
    #        os.environ['DB_PASSWORD'],
    #        os.environ['DB_HOST'],
    #        os.environ['DATABASE_NAME'],
    #    )
    
    # As of Flask-SQLAlchemy 2.4.0 it is easy to pass in options directly to the
    # underlying engine. This option makes sure that DB connections from the
    # pool are still valid. Important for entire application since
    # many DBaaS options automatically close idle connections.
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
