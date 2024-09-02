from typing import List

from flask_sqlalchemy import SQLAlchemy

from ...models.models import ( 
    Category, 
    ListingDraft, 
    SubCategory,
    Vendor,
)


def select_vendor(db: SQLAlchemy, uid: int) -> Vendor|None:
    """Select & return vendor object from user id provided 
    """
    return db.session.scalar(db.select(Vendor).where(
        Vendor.user_id==uid))


def select_categories(db: SQLAlchemy) -> List[Category]:
    return db.session.scalars(db.select(Category)).all()


def select_sub_categories(db: SQLAlchemy) -> List[SubCategory]:
    return db.session.scalars(db.select(SubCategory)).all()


def select_draft_or_404(db: SQLAlchemy, uuid: str) -> ListingDraft|None:
    return db.session.scalar(db.select(ListingDraft).where(
        ListingDraft.uuid==uuid))
