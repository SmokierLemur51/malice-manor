from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .models.base import Base


db = SQLAlchemy(model_class=Base)


fbcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "users.login"
