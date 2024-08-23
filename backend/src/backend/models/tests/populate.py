from flask_sqlalchemy import SQLAlchemy
from ..models import Category, SubCategory, Role
from typing import List

from sqlalchemy.exc import IntegrityError

from ..queries import parse_for_category_id


def populate_roles(db: SQLAlchemy):
    roles = [
        Role(name="customer", info="General Customer, can only access market and forum."),
        Role(name="moderator", 
            info="No market access, can only access forum to moderate threads."),
        Role(name="vendor", info="Can access market, forum, and vendor portal. Can create vendor-employee accounts."),
        Role(name="admin", info="Market and forum administrators.")
    ]
    try:
        db.session.add_all(roles)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)



def populate_categories(db: SQLAlchemy) -> None:
    categories = [
        Category(
            category="Books",
            info="All books.",
        ),
        Category(
            category="Cursed Items",
            info="Generally cursed items.",
        ),
        Category(
            category="Potions",
            info="Potions parent category",
        ),
        Category(
            category="Contraband",
            info="General contraband",
        ),
        Category(
            category="Items",
            info="Non cursed, physical possessions. Brooms, charmed objects, etc.",
        ),
        Category(
            category="Magical Creatures",
            info="Magical Creatures for sale.",
        ),
        Category(
            category="Services",
            info="Your services for sale.",
        ),
        Category(
            category="Misc",
            info="Dump anything else here for now.",
        )
    ]
    try:
        db.session.add_all(categories)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print(IntegrityError)



def populate_sub_categories(db: SQLAlchemy) -> None:
    categories = db.session.scalars(db.select(Category)).all()
    sub_categories = [
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Dark Wizard Manifestos",
            info="Manifestos of dark wizards, **We do not promote/allow any kind of racism or racist content.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Banned Books",
            info="Book's currently banned under law.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Restricted Section",
            info="Books that can be found in the Hogwarts restricted section.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Spell Books.",
            info="General spell books.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "books"),
            sub_category="Curse Books",
            info="Books for learning curses.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "potions"),
            sub_category="Personal Enhancement",
            info="Personally enhancing potions, physical traits, appearances or modification of behavior.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "potions"),
            sub_category="Love Potions",
            info="Love potions, love at first sight...",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "potions"),
            sub_category="Dangerous Potions",
            info="Potions meant to kill, maim, or in other ways cause general suffering.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "items"),
            sub_category="Cursed Items",
            info="Cursed brooms, bludgers that kill, jewlrey. Dangerous cursed items.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "items"),
            sub_category="Charmed Items",
            info="Undetectable extension bags, enchanted tools, etc.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "magical creatures"),
            sub_category="Exotic Creatures",
            info="Imported, dangerous magical creatures.",
        ),
        SubCategory(
            parent_category_id=parse_for_category_id(categories, "magical creatures"),
            sub_category="Endangered Creatures",
            info="Endangered magical creatures, in most cases illegal to hunt or own.",
        ),
    ]
    try:
        db.session.add_all(sub_categories)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print(e)