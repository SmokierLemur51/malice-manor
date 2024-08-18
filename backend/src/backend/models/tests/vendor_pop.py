""" Depreciated 

from flask_sqlalchemy import SQLAlchemy
from flask import current_app

from sqlalchemy.exc import IntegrityError

from ..models import Vendor



def populate_vendors(db: SQLAlchemy) -> None:
    sample_vendors = [
        Vendor(
            private_username="arkansasbimbo",
            public_username="billcocaineclinton",
            secret_phrase="he definitely did it",
        ),
        Vendor(
            private_username="privategary",
            public_username="billkilledgary",
            secret_phrase="sandanista government",
        ),
        Vendor(
            private_username="cocainekingpin",
            public_username="pabloescobar",
            secret_phrase="testing the secret phrase",
        ),
        Vendor(
            private_username="souplover",
            public_username="potionmaster",
            secret_phrase="the us government knew",
        ),
        Vendor(
            private_username="logansama",
            public_username="khanlogan",
            secret_phrase="logan the great of corydon",
        ),
    ]
    with current_app.app_context():
            try:
                db.session.add_all(sample_vendors)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                print(f"Vendor(s) already exist. Error:\n{e}")
"""