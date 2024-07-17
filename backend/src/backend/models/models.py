"""
File: models.py
Author: Logan Lee

This file defines the models to be used in the web application.
"""
import datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Vendor(Base):
    __tablename__ = "vendors"
    id: Mapped[int] = mapped_column(primary_key=True)
    private_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    public_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    secret_phrase: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    hashed_pw: Mapped[str] = mapped_column(String(60), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=1)

    listings: Mapped[List['Listing']] = relationship(back_populates='vendor')

    def __repr__(self) -> str:
        return "{}".format(self.private_username)
    
    def sign_message(self, message: str) -> str: # sign message with self.priv_key
        return message

    def encrypt_message(self, message: str) -> str: # encrypt message with customer.pub_key
        return message

    def decrypt_message(self, message: str) -> str: # decrypt message from sender using self.pub_key
        return message

    def verify_message(self, message: str) -> str: # verify messages were sent by customer
        return message


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    private_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    public_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    secret_phrase: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)

    # orders: Mapped[List["Order"]] = relationship(back_populates="customer")
    cart: Mapped["Cart"] = relationship(back_populates="customer")

    def __repr__(self) -> str:
        return "{}".format(self.private_username)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)

    # relationships
    listings: Mapped[List["Listing"]] = relationship(back_populates='category')
    sub_categories: Mapped[List["SubCategory"]] = relationship(back_populates="parent_category")

    def __repr__(self) -> str:
        return "{}".format(self.category)


class SubCategory(Base):
    __tablename__ = "sub_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    sub_category: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)

    # relationship
    parent_category: Mapped["Category"] = relationship(back_populates="sub_categories")
    listings: Mapped[List["Listing"]] = relationship(back_populates="sub_category")

    def __repr__(self) -> str:
        return "Sub Category: <{}>, Parent Category: <{}>".format(
            self.sub_category, self.parent_category.category)


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

    # relationships
    vendor: Mapped['Vendor'] = relationship(back_populates='listings')
    category: Mapped['Category'] = relationship(back_populates='listings')
    sub_category: Mapped['SubCategory'] = relationship(back_populates='listings')
    cart_items: Mapped[List["CartItem"]] = relationship(back_populates="listing")

    def __repr__(self) -> str:
        return "Listing: {}, Vendor: {}".format(self.name, self.vendor.public_username)


class Cart(Base):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    paid_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    ordered_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    total: Mapped[float] = mapped_column(Float)

    customer: Mapped["Customer"] = relationship(back_populates="cart")
    items: Mapped[List["CartItem"]] = relationship(back_populates="cart")

    def __repr__(self) -> str:
        return self.customer.public_username

    def get_total(self) -> None:
        self.total = 0.0    # reset to 0 before looping through cart
        for i in items:
            self.total += i.price

    
class CartItem(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    price: Mapped[float] = mapped_column(Float)

    cart: Mapped["Cart"] = relationship(back_populates="items")
    listing: Mapped["Listing"] = relationship(back_populates="cart_items")

    def __repr__(self) -> str:
        return self.product.name


class Order():
    pass


class Escrow():
    pass


class Dispute():
    pass


class VendorReview():
    pass


class ListingReview():
    pass



