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


class Status(Base):
    __tablename__ = "statuses"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return "{}".format(self.status)


class Vendor(Base):
    __tablename__ = "vendors"
    id: Mapped[int] = mapped_column(primary_key=True)
    private_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    public_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    secret_phrase: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)

    products: Mapped[List['Product']] = relationship(back_populates='vendor')

    def __repr__(self) -> str:
        return "{}".format(self.private_username)


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    private_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    public_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    secret_phrase: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)

    orders: Mapped[List["Order"]] = relationship(back_populates="customer")

    def __repr__(self) -> str:
        return "{}".format(self.private_username)


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)

    # relationships
    products: Mapped[List["Product"]] = relationship(back_populates='category')
    sub_categories: Mapped[List["ProductSubCategory"]] = relationship(back_populates="parent_category")

    def __repr__(self) -> str:
        return "{}".format(self.category)


class ProductSubCategory(Base):
    __tablename__ = "product_sub_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_category_id: Mapped[int] = mapped_column(ForeignKey("product_categories.id"))
    sub_category: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)

    # relationships
    parent_category: Mapped["ProductCategory"] = relationship(back_populates="sub_categories")
    products: Mapped[List["Product"]] = relationship(back_populates="sub_category")

    def __repr__(self) -> str:
        return "Sub Category: <{}>, Parent Category: <{}>".format(
            self.sub_category, self.parent_category.category)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('product_categories.id'), nullable=True)
    sub_category_id: Mapped[int] = mapped_column(ForeignKey('product_sub_categories.id'))
    vendor_id: Mapped[int] = mapped_column(ForeignKey('vendors.id'))
    # The vendor must provide information about their units of measurement.
    # Ex:
    #   Using milliliters vs fluid ounces
    uom: Mapped[str] = mapped_column(String(100))
    # Total amount of the units of measurement the listing is offering.
    # Ex:
    #   5 of the 150 millileter vials of liquid luck.
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    # Vendor will provide info about the quantity that is offered.
    quantity_info: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    info: Mapped[str] = mapped_column(String(500), nullable=True)
    selling: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # relationships
    uom: Mapped['UnitOfMeasurement'] = relationship(back_populates='products')
    vendor: Mapped['Vendor'] = relationship(back_populates='products')
    category: Mapped['ProductCategory'] = relationship(back_populates='products')
    sub_category: Mapped['ProductSubCategory'] = relationship(back_populates='products')


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    price: Mapped[float] = mapped_column(Float, default=0.0)

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")
    escrow: Mapped["Escrow"] = relationship(back_populates="order")


class Escrow(Base):
    __tablename__ = "escrows"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    deposited: Mapped[bool] = mapped_column(Boolean, default=False)
    shipped: Mapped[bool] = mapped_column(Boolean, default=False)
    received: Mapped[bool] = mapped_column(Boolean, default=False)
    paid: Mapped[bool] = mapped_column(Boolean, default=False)

    order: Mapped["Order"] = relationship(back_populates="escrow")

    def __repr__(self) -> str:
        return "Escrow {}".format(self.id)


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    order: Mapped["Order"] = relationship(back_populates="order_items")
    product: Mapped["Product"] = relationship(back_populates="order_items")
