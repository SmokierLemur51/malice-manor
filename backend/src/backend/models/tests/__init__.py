from flask_sqlalchemy import SQLAlchemy


def populate_users(db: SQLAlchemy):
    users = [
        User(
            role_id=load_role(db, "customer").id,
            private_username="private",
            public_username="public",
            password=fbcrypt.generate_password_hash("password"),
            secret_key=generate_secret_key(),
        ),
        User(
            role_id=load_role(db, "customer").id,
            private_username="x",
            public_username="y",
            password=fbcrypt.generate_password_hash("password"),
            secret_key=generate_secret_key(),
        ),
        User(
            role_id=load_role(db, "vendor").id,
            private_username="vendorpriv",
            public_username="pubvendor",
            password=fbcrypt.generate_password_hash("password"),
            secret_key=generate_secret_key(),
        ),
    ]
    try:
        db.session.add_all(users)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)