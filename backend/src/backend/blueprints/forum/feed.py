""" 
Some things our feed should handle. 

Loading posts:
-top
-hot
-new
-by topic
"""
from flask_sqlalchemy import SQLAlchemy

from . import queries
from ...models.models import (
    ForumCommunity,
    ForumPost,
)

# top posts
def top_posts(db: SQLAlchemy, c: ForumCommunity, f: str) -> List[ForumPost]:
    if f == "all":
        db.session.scalars(db.select(ForumPost)).all()
    elif f == "year":
        db.session.scalars(db.select(ForumPost)).all()
    elif f == "month":
        db.session.scalars(db.select(ForumPost)).all()
    elif f == "week":
        db.session.scalars(db.select(ForumPost)).all()
    elif f == "day":
        db.session.scalars(db.select(ForumPost)).all()
    else:
        db.session.scalars(db.select(ForumPost)).all()