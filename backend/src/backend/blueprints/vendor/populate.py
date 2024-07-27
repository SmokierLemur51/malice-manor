"""
Module: vendors.populate
Description: 
"""
from typing import List
from quart import g

values = ['cold', 'water', 'chirp', 'sand', 'blues', 'math', 
          'rave', 'bottle', 'paper', 'note', 'clean', 'charge']

class Vendor:
    def __init__(self, private_username, public_username, secret_phrase):
        self.private_username = private_username
        self.public_username = public_username
        self.secret_phrase = secret_phrase


async def populate_vendors():
    obj_list = [
        Vendor(
            private_username="voldemort", 
            public_username="room_of_requirements",
            secret_phrase="spells cookies charms",
        ),
        Vendor(
            private_username="darkwizard", 
            public_username="wizardman",
            secret_phrase="wizards watermelons water",
        ),
        Vendor(
            private_username="misspotion", 
            public_username="thepotionqueen",
            secret_phrase="potions parties powder",
        ),
        Vendor(
            private_username="gillyweeder", 
            public_username="the_botanist",
            secret_phrase="bears beets battlestar galactica",
        ),
        Vendor(
            private_username="scarewolf", 
            public_username="the_werewolf",
            secret_phrase="fur fun funky",
        ),
    ]
    for v in obj_list:
        await g.connection.execute(
            """INSERT INTO vendors (public_username, private_username, secret_phrase) 
            VALUES (:public, :private, :secret)""",
            {'public': v.public_username, 'private': v.private_username, 'secret': v.secret_phrase}
        )

