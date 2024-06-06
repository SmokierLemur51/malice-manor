""" File: models/tests/category_pop.py


"""
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

from sqlalchemy.exc import IntegrityError

from ..models import ProductCategory, ProductSubCategorys

def populate_categories(db: SQLAlchemy) -> None:
    categories = [
        ProductCategory(
            category="Books",
            info="All books.",
        ),
        ProductCategory(
            category="Cursed Items",
            info="Generally cursed items.",
        ),
        ProductCategory(
            category="Potions",
            info="Potions parent category",
        ),
        ProductCategory(
            category="Contraband",
            info="General contraband",
        ),
        ProductCategory(
            category="Items",
            info="Non cursed, physical possessions. Brooms, charmed objects, etc.",
        ),
        ProductCategory(
            category="Magical Creatures",
            info="Magical Creatures for sale.",
        ),
        ProductCategory(
            category="Services",
            info="Your services for sale.",
        ),
        ProductCategory(
            category="Misc",
            info="Dump anything else here for now.",
        )
    ]
    with current_app.app_context():
        try:
            db.session.add_all(categories)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(IntegrityError)


def parse_for_category_id(categories: List[ProductCategory], term: str) -> int:
    """ 
    Params:
    -categories: List[ProductCategory], list of categories to parse through.
    -term: str, search term, non case sensitive, it recieves .title() string method
    """
    for c in categories:
        if c.category == term.title():
            return c.id
    return 0



def populate_sub_categories(db: SQLAlchemy) -> None:
    categories = db.session.scalars(db.select(ProductCategories)).all()
    sub_categories = [
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Dark Wizard Manifestos",
            info="Manifestos of dark wizards, **We do not promote/allow any kind of racism or racist content.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Banned Books",
            info="Book's currently banned under law.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Restricted Section",
            info="Books that can be found in the Hogwarts restricted section.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Spell Books.",
            info="General spell books.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Curse Books",
            info="Books for learning curses.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "potions"),
            sub_category="Personal Enhancement",
            info="Personally enhancing potions, physical traits, appearances or modification of behavior.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "potions"),
            sub_category="Love Potions",
            info="Love potions, love at first sight...",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "potions"),
            sub_category="Dangerous Potions",
            info="Potions meant to kill, maim, or in other ways cause general suffering.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "items"),
            sub_category="Cursed Items",
            info="Cursed brooms, bludgers that kill, jewlrey. Dangerous cursed items.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "items"),
            sub_category="Charmed Items",
            info="Undetectable extension bags, enchanted tools, etc.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "magical creatures"),
            sub_category="Exotic Creatures",
            info="Imported, dangerous magical creatures.",
        ),
        ProductSubCategory(
            parent_category_id=parse_for_category_id(categories, "magical creatures"),
            sub_category="Endangered Creatures",
            info="Endangered magical creatures, in most cases illegal to hunt or own.",
        ),
    ]
    with current_app.app_context():
        try:
            db.session.add_all(sub_categories)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(e)