from typing import List

from flask_sqlalchemy import SQLAlchemy

from ...models.models import ForumCommunity, ForumPost


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


def select_community(db: SQLAlchemy, n: str) -> ForumCommunity|None:
    return db.session.scalar(db.select(ForumCommunity).where(ForumCommunity.name == n))


def select_communities(db: SQLAlchemy) -> List[ForumCommunity]|None:
    return db.session.scalars(db.select(ForumCommunity)).all()


def select_post(db: SQLAlchemy, ) -> ForumPost|None:
    return None

def select_posts(
        db: SQLAlchemy, 
        c: ForumCommunity|None, 
        filter: str, 
        quanity: int|None,
    ) -> List[ForumPost]:
    """ 
    Select posts from a provided community via filter & quanity.

    :param c:
        ForumCommunity obj instance to query posts from.
    :param filter:
        String.lower() to filter posts by, options are
        -all
        -top
        -hot
        -new (default)
    :param quantity:
        Integer quanity of ForumPost objects returned.
    """
    if filter.lower() == "all":
        if quanity is None or quanity == 0:
            return db.session.scalars(db.select(ForumPost).where(ForumPost.community_id == c.id)).all()
        else:
            return db.session.scalars(db.select(ForumPost).where(ForumPost.community_id == c.id)).limit(quanity)
    return []


