import flask
from flask_sqlalchemy import SQLAlchemy
from ..models import Role


def populate_roles(db: SQLAlchemy):
    roles = [
        Role(name="customer", info="General Customer, can only access market and forum."),
        Role(name="moderator", 
            info="No market access, can only access forum to moderate threads."),
        Role(name="vendor", info="Can access market, forum, and vendor portal. Can create vendor-employee accounts."),
        Role(name="admin", info="Market and forum administrators.")
    ]
    with flask.current_app.app_context():
        try:
            db.session.add_all(roles)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)

