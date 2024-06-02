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
        return "{}".format(self.vendor)

        

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



# This product will not be associated with a warehouse, Product.id will be referenced
# in the InventoryItem class.
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())    
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('product_categories.id'))
    sub_category_id: Mapped[int] = mapped_column(ForeignKey('product_sub_categories.id'))    
    vendor_id: Mapped[int] = mapped_column(ForeignKey('vendors.id'))
    title: Mapped[str] = mapped_column(String(120), unique=True)
    selling: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    # need to add sizing dimensions

    # relationships
    vendor: Mapped['Vendor'] = relationship(back_populates="products")
    category: Mapped['ProductCategory'] = relationship(back_populates='products')
    sub_category: Mapped['ProductCategory'] = relationship(back_populates='products')
    


class Cart(Base):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)