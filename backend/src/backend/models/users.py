from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from .base import Base
from ..extension import login_manager

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


