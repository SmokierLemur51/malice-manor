from typing import List
from flask_sqlalchemy import SQLAlchemy

from ...models.models import Vendor
from ...extensions import fbcrypt

def vendors(db: SQLAlchemy) -> None:
    vendors = [
        Vendor(
            private_username="", 
            public_username="",
            secret_phrase="",
            hashed_pw=fbcrypt.generate_password_hash()
        ),
    ]
