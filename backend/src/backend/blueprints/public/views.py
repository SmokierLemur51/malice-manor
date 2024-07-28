import os

from flask import Blueprint, flash,redirect, render_template, url_for, request, current_app
from flask_login import login_user

from .forms import RegisterUserForm, RegisterVendorForm, LoginForm

from ...extensions import fbcrypt, login_manager
from ...models.models import db
from ...models.models import User, Vendor
from ...models import queries
from ...toolbox.helpers import generate_secret_key


public = Blueprint('public', __name__, template_folder="templates/public", url_prefix="/")


@public.route("/populate")
def populate():
    from ...models.tests.roles import populate_roles
    populate_roles(db)
    return redirect(url_for('public.index'))

# test route
@public.route("/vendors")
def vendors():
    vendors = db.session.scalars(db.select(Vendor)).all()
    return render_template("x.html", vendors=vendors)


@public.route("/")
def index():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("index.html", elements=elements)


# This is probably not the best version
@public.route("/login")
def login():
    elements = {"title": "Login"}
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.private_username == form.private_username.data)).first()
        if user and fbcrypt.check_password_hash(user.password, form.private_username.data):
            login_user(user)
            if user.role.name == "vendor":
                return redirect(url_for('vendor.index'))
            elif user.role.name == "moderator":
                return redirect(url_for('forum.index'))
            elif user.role.name == "admin":
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('market.index'))
    return render_template("login.html", elements=elements)


@public.route("/register-customer", methods=["GET", "POST"])
def register_customer():
    elements = {"title": "Register Market Account"}
    form = RegisterVendorForm()
    if form.validate_on_submit():
        if form.password.data == form.password_match.data:
            u = User(
                role_id=queries.load_role(db, "customer").id,
                public_username=form.public_username.data,
                private_username=form.private_username.data,
                password=fbcrypt.generate_password_hash(form.password.data),
                secret_key=generate_secret_key(),
            )
            with current_app.app_context():    
                with db.session.begin():
                    try:
                        db.session.add(u)
                        db.session.flush()
                        # new vendor
                        c = Customer(user_id=u.id)
                        db.session.add(c)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(e)
            return redirect(url_for("public.login"))
        else:
            flash("Passwords must match.")
            return render_template("register_vendor.html", elements=elements, form=form)
    return render_template("register_customer.html")


@public.route("/register-vendor", methods=["GET", "POST"])
def register_vendor():
    elements = {"title": "Register Vendor Account"}
    form = RegisterVendorForm()
    if form.validate_on_submit():
        if form.password.data == form.password_match.data:
            u = User(
                role_id=queries.load_role(db, "vendor").id,
                public_username=form.public_username.data,
                private_username=form.private_username.data,
                password=fbcrypt.generate_password_hash(form.password.data),
                secret_key=generate_secret_key(),
            )
            with current_app.app_context():    
                with db.session.begin():
                    try:
                        db.session.add(u)
                        db.session.flush()
                        # new vendor
                        v = Vendor(user_id=u.id)
                        db.session.add(v)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(e)
            return redirect(url_for("public.login"))
        else:
            flash("Passwords must match.")
            return render_template("register_vendor.html", elements=elements, form=form)
    return render_template("register_vendor.html", elements=elements, form=form)


@public.route("/moderator-application")
def moderator_application():
    return redirect(url_for('public.index'))

"""
    form = ContactRequestForm()
    if form.validate_on_submit():
        new_ = ContactRequest(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            message=form.message.data,
        )
        with current_app.app_context():    
            db.session.add(new_)
            db.session.commit()
        flash("Thank you! We will be in touch.")
        return redirect(url_for("public.index"))

"""
