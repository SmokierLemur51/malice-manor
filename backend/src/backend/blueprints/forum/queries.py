from flask_sqlalchemy import SQLAlchemy

from ...models.models import ForumCommunity


def check_unique(db: SQLAlchemy, n: str) -> bool:
        try:
            existing = db.session.scalar(db.select(ForumCommunity).where(ForumCommunity.name == n))
            # Check and make sure it is none
            if existing is None:
                print("Unque community name provided.")
                return True
            else:
                print("Community name taken.")
                return False
        except AttributeError as e: 
            return False 


def query_community(db: SQLAlchemy, n: str) -> ForumCommunity|None:
    return db.session.scalar(db.select(ForumCommunity).where(ForumCommunity.name == n))