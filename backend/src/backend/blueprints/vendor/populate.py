"""
Module: vendors.populate
Description: 
"""
from typing import List
from flask_sqlalchemy import SQLAlchemy

from ...models.models import Vendor
from ...extensions import fbcrypt
from ...toolbox import helpers

values = ['cold', 'water', 'chirp', 'sand', 'blues', 'math', 
          'rave', 'bottle', 'paper', 'note', 'clean', 'charge']

def vendors(db: SQLAlchemy) -> None:
    vendors = [
        Vendor(
            private_username="cocainemaster", 
            public_username="pabloescobar",
            secret_phrase="cocaine cookies coochie",
            hashed_pw=fbcrypt.generate_password_hash(helpers.convert_list_string(helpers.pick_random_choices(values, 3)))
        ),
        Vendor(
            private_username="darkwizard", 
            public_username="wizardman",
            secret_phrase="wizards watermelons water",
            hashed_pw=fbcrypt.generate_password_hash(helpers.convert_list_string(helpers.pick_random_choices(values, 3)))
        ),
        Vendor(
            private_username="misspotion", 
            public_username="thepotionqueen",
            secret_phrase="potions parties powder",
            hashed_pw=fbcrypt.generate_password_hash(helpers.convert_list_string(helpers.pick_random_choices(values, 3)))
        ),
        Vendor(
            private_username="", 
            public_username="",
            secret_phrase="",
            hashed_pw=fbcrypt.generate_password_hash(helpers.convert_list_string(helpers.pick_random_choices(values, 3)))
        ),
        Vendor(
            private_username="", 
            public_username="",
            secret_phrase="",
            hashed_pw=fbcrypt.generate_password_hash(helpers.convert_list_string(helpers.pick_random_choices(values, 3)))
        ),
]
