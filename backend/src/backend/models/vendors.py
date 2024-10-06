from typing import List

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Vendor(Base):
    __tablename__ = "vendors"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # Used to check if user has setup vendor account. 
    setup: Mapped[bool] = mapped_column(Boolean, default=False)
    # Approved bool will control if vendor can make forum posts or list products.
    approved: Mapped[bool] = mapped_column(Boolean, default=True)
    public_key: Mapped[str] = mapped_column(String(500), nullable=True)
    # Generated at creation, displayed to user, and hashed forever. 
    recovery_hash: Mapped[str] = mapped_column(String(60))
    # User created value, hashed and used on withdraw. 
    withdrawl_pin: Mapped[str] = mapped_column(String(60))
    # Based off of completed orders and reviews. 
    score: Mapped[int] = mapped_column(Integer, default=0)
    # Each order can be reviewed by customer, each new review will trigger a re-calculation.
    average_review: Mapped[float] = mapped_column(Float, default=0.0)

    user: Mapped["User"] = relationship(back_populates="vendor")
    listing_drafts: Mapped[List['ListingDraft']] = relationship(back_populates='vendor')
    listings: Mapped[List['Listing']] = relationship(back_populates='vendor')

    def __repr__(self) -> str:
        return "{}".format(self.private_username)


