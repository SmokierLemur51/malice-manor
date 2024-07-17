"""
Module: vendors.populate
Description: 
"""
from typing import List
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

from ...models.models import Vendor
from ...extensions import fbcrypt
from ...toolbox import helpers

values = ['cold', 'water', 'chirp', 'sand', 'blues', 'math', 
          'rave', 'bottle', 'paper', 'note', 'clean', 'charge']

def populate_vendors(db: SQLAlchemy) -> None:
    vendors = [
        Vendor(
            private_username="voldemort", 
            public_username="room_of_requirements",
            secret_phrase="spells cookies charms",
            hashed_pw=fbcrypt.generate_password_hash(
                helpers.convert_list_string(helpers.pick_random_choices(values, 3))),
        ),
        Vendor(
            private_username="darkwizard", 
            public_username="wizardman",
            secret_phrase="wizards watermelons water",
            hashed_pw=fbcrypt.generate_password_hash(
                helpers.convert_list_string(helpers.pick_random_choices(values, 3))),
        ),
        Vendor(
            private_username="misspotion", 
            public_username="thepotionqueen",
            secret_phrase="potions parties powder",
            hashed_pw=fbcrypt.generate_password_hash(
                helpers.convert_list_string(helpers.pick_random_choices(values, 3))),
        ),
        Vendor(
            private_username="gillyweeder", 
            public_username="the_botanist",
            secret_phrase="bears beets battlestar galactica",
            hashed_pw=fbcrypt.generate_password_hash(
                helpers.convert_list_string(helpers.pick_random_choices(values, 3))),
        ),
        Vendor(
            private_username="scarewolf", 
            public_username="the_werewolf",
            secret_phrase="fur fun funky",
            hashed_pw=fbcrypt.generate_password_hash(
                helpers.convert_list_string(helpers.pick_random_choices(values, 3))),
        ),
    ]
    with current_app.app_context():
        try:
            db.session.add_all(vendors)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
