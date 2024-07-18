from typing import List
from flask_sqlalchemy import SQLAlchemy

from ...models.models import (
    db,
    Customer,
    Listing,
    Vendor,
)


def vendors(db: SQLAlchemy) -> List[Vendor]:
    return db.session.scalars(db.select(Vendor)).all()


def where_vendor(db: SQLAlchemy, **where) -> List[Vendor]:
    """
    Generate query providing a dictionary of 'where x and y' statements
    """
    conditions = [getattr(Vendor, key) == value for key, value in where.items()]
    return db.session.scalars(db.select(Vendor).where(and_(*conditions))).all()


def customers(db: SQLAlchemy) -> List[Customer]:
    return db.session.scalars(db.select(Customer)).all()


def listings(db: SQLAlchemy) -> List[Listing]:
    return db.session.scalars(db.select(Listing)).all()
