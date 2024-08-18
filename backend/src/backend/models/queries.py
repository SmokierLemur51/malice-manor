"""
File: models/queries.py
Author: Logan Lee 28-July-2024

Common queries for the application. 
"""
from typing import List
from flask_sqlalchemy import SQLAlchemy

from .models import (
    Category,
    SubCategory,
    Role,
    User,
    Vendor,
)


def load_role(db: SQLAlchemy, r: str) -> Role:
    return db.session.scalars(db.select(Role).where(Role.name == r)).first()


def check_duplicate_username(db: SQLAlchemy, u: str) -> bool:
    if db.session.scalar(db.select(User).where(User.public_username == u)).first():
        return True
    

def query_user(db: SQLAlchemy, priv: str) -> User|None:
    return db.session.scalar(db.Select(User).where(User.private_username == priv)).first()


def parse_for_category_id(categories: List[Category], term: str) -> int:
    """ 
    Params:
    -categories: List[Category], list of categories to parse through.
    -term: str, search term, non-case-sensitive, it receives .title() string method
    """
    for c in categories:
        if c.category == term.title():
            return c.id
    return 0


def parse_for_sub_category_id(sub_categories: List[SubCategory], term: str) -> SubCategory:
    """
    Params:
    -categories: List[SubCategory], list of categories to parse through.
    -term: str, search term, non-case-sensitive, it receives .title() string method
    """
    for c in sub_categories:
        if c.sub_category == term.title():
            return c
    return SubCategory()


def parse_for_vendor_id(vendors: List[Vendor], term: str) -> Vendor:
    """
    Params:
    -categories: List[Vendor], list of vendors to parse through.
    -term: str, search term, non-case-sensitive, it receives .title() string method
    """
    for v in vendors:
        if v.public_username == term.title():
            return v
    return Vendor()