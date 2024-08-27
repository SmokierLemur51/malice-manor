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
from flask_login import UserMixin

from ..extensions import login_manager


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    info: Mapped[str] = mapped_column(String(250), nullable=True)

    users: Mapped[List["User"]] = relationship(back_populates="role")
    
    def __repr__(self) -> str:
        return self.name


class User(Base, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))    
    private_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    public_username: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    secret_key: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    
    role: Mapped["Role"] = relationship(back_populates="users")                                        
    vendor: Mapped["Vendor"] = relationship(back_populates="user")
    customer: Mapped["Customer"] = relationship(back_populates="user")
    listing_comments: Mapped[List['ListingComment']] =relationship(back_populates='author')    
    posts: Mapped[List['ForumPost']] = relationship(back_populates='author')
    post_comments: Mapped[List['PostComment']] = relationship(back_populates='author')
    forum_communities_owned: Mapped[List['ForumCommunity']] = relationship(back_populates='owner')
    

    def __repr__(self) -> str:
        return self.public_username


@login_manager.user_loader
def load_user(user_id):
    return db.session.scalar(db.select(User).where(User.id == user_id))



class Vendor(Base):
    __tablename__ = "vendors"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    score: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="vendor")
    listings: Mapped[List['Listing']] = relationship(back_populates='vendor')

    def __repr__(self) -> str:
        return "{}".format(self.private_username)


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    score: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="customer")

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


class ForumCommunity(Base):
    __tablename__ = "forum_communities"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(60), unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    owner: Mapped['User'] = relationship(back_populates='forum_communities_owned')
    posts: Mapped[List['ForumPost']] = relationship(back_populates='community')

    def __repr__(self) -> str:
        return self.name

    def check_name_no_spaces(self) -> bool:
        """ Check for spaces in community name, should be none.
            Return False if there are any.
        """
        return True


class ForumPost(Base):
    __tablename__ = "forum_posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    community_id: Mapped[int] = mapped_column(ForeignKey('forum_communities.id'))
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(String(1500), nullable=True)
    slug: Mapped[str] = mapped_column(String(250), nullable=False)
    token: Mapped[str] = mapped_column(String(80), nullable=False)

    author: Mapped['User'] = relationship(back_populates='posts')
    community: Mapped['ForumCommunity'] = relationship(back_populates='posts')
    post_comments: Mapped[List['PostComment']] = relationship(back_populates='post')

    def __repr__(self) -> str:
        return self.title


# Needs to add 
class PostComment(Base):
    __tablename__ = "forum_post_comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('forum_posts.id'))
    comment: Mapped[str] = mapped_column(String(1500), nullable=True)

    author: Mapped['User'] = relationship(back_populates='post_comments')
    post: Mapped['ForumPost'] = relationship(back_populates='post_comments')

    def __repr__(self) -> str:
        return "User {} Comment".format(self.author.public_username)    