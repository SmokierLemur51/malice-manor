from typing import List
from flask_sqlalchemy import SQLAlchemy

from ...models.models import (
    User
)

def get_user(db: SQLAlchemy, u: str) -> User|None:
    """Loading user for flask_login
    :param db: flask_sqlalchemy object.
    :param u: username
    """
    try:
        u = db.session.scalar(db.select(User).where(User.username == u))
        return u
    except AttributeError:
        return None


def check_usernames(db: SQLAlchemy, pub: str, priv: str) -> bool:
    """ 
    """
    pub_check = db.session.scalar(db.select(User).where(User.public_username == pub))
    priv_check = db.session.scalar(db.select(User).where(User.private_username == priv))
    if pub_check and priv_check == None:
        return False
