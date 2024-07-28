"""
File: models/queries.py
Author: Logan Lee 28-July-2024

Common queries for the application. 
"""
from typing import List
from flask_sqlalchemy import SQLAlchemy

from .models import User, Role


def load_role(db: SQLAlchemy, r: str) -> Role:
    return db.session.scalars(db.select(Role).where(Role.name == r)).first()


def check_duplicate_username(db: SQLAlchemy, u: str) -> bool:
    if db.session.scalar(db.select(User).where(User.public_username == u)).first():
        return True
    