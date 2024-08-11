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
        u = db.session.scalar(db.select(User).where(User.private_username == u))
        return u
    except TypeError:
        return None



def check_unique_usernames(db: SQLAlchemy, pub: str, priv: str) -> bool:
    """ 
    """
    try:
        if db.session.scalar(db.select(User).where(User.private_username == priv)):
            print("no result")
            return False
    except Exception as e:
        print(Exception)
        return False 
    