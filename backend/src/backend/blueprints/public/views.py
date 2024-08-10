import os

from flask import Blueprint, flash,redirect, render_template, url_for, request, current_app
from flask_login import login_user

from ...models.models import db


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
    # query latest info
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("index.html", elements=elements)

