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
        if u is None:
            print("No user found...")
            return None
        else:
            return u
    except Exception as e:
        print("Excetption: ", e)
        return None



# Might be best to rename to something like unique_usernames
def check_unique_usernames(db: SQLAlchemy, priv: str, pub: str) -> bool:
    """ 
    """
    try:
        # We have to execute several queries here:
        # Private-Private, Private-Public, Public-Private, Public-Public
        # I think all users should have completely unique usernames.
        priv_priv = db.session.scalar(db.select(User).where(User.private_username == priv))
        priv_pub = db.session.scalar(db.select(User).where(User.public_username == priv))
        pub_priv = db.session.scalar(db.select(User).where(User.private_username == pub))
        pub_pub = db.session.scalar(db.select(User).where(User.public_username == pub))
        # Check all are None
        if priv_priv is None and priv_pub is None and pub_priv is None and pub_pub is None:
            print("Usernames provided are unique.")
            return True
        else:
            print("Usernames are not unique.")
            return False
    except AttributeError as e: 
        return False 
    