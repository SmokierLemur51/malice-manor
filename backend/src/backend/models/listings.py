import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)
    sub_category_id: Mapped[int] = mapped_column(ForeignKey('sub_categories.id'))
    vendor_id: Mapped[int] = mapped_column(ForeignKey('vendors.id'))
   
    name: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)
    selling: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    uuid: Mapped[str] = mapped_column(String(120), nullable=False)

    # relationships
    vendor: Mapped['Vendor'] = relationship(back_populates='listings')
    category: Mapped['Category'] = relationship(back_populates='listings')
    sub_category: Mapped['SubCategory'] = relationship(back_populates='listings')
    listing_comments: Mapped[List['ListingComment']] = relationship(back_populates='listing')
    cart_items: Mapped[List["CartItem"]] = relationship(back_populates="listing")

    def __repr__(self) -> str:
        return "Listing: {}, Vendor: {}".format(self.name, self.vendor.public_username)


class ListingComment(Base):
    __tablename__ = "listing_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey('listings.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    commment: Mapped[str] = mapped_column(String(1000), nullable=False)

    listing: Mapped['Listing'] = relationship(back_populates='listing_comments')
    author: Mapped['User'] = relationship(back_populates='listing_comments')
