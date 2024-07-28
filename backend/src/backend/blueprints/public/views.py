import os

from flask import Blueprint, redirect, render_template, url_for, request, current_app

from .forms import RegisterUserForm, RegisterVendorForm

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
    v = db.session.scalars(db.select(Vendor)).all()
    return v[0].user.private_username




@public.route("/")
def index():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("index.html", elements=elements)



@public.route("/create-account")
def create_account():
    elements={
            "title": "Create Account",
            "market_name": os.environ["MARKET_NAME"],
        }
    return render_template("create_account.html", elements=elements)


@public.route("/login")
def login():
    elements={
            "title": "Login",
            "market_name": os.environ["MARKET_NAME"],
        }
    return render_template("login.html", elements=elements)


@public.route("/register-customer", methods=["GET", "POST"])
def register_customer():
    return render_template("register_customer.html")


@public.route("/register-vendor", methods=["GET", "POST"])
def register_vendor():
    elements = {"title": "Register Vendor Account"}
    form = RegisterVendorForm()
    if form.validate_on_submit():
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
        return redirect(url_for("public.vendors"))
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
