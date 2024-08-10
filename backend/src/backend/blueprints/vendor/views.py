import os

from flask import Blueprint, redirect, render_template, url_for, request, current_app
from flask_login import current_user, login_required

from ...models.models import db, Vendor


vendor = Blueprint('vendor', __name__, template_folder="templates/vendor", url_prefix="/vendors")


@vendor.route("/populate")
def populate():
    from .populate import populate_vendors
    populate_vendors(db)
    return redirect(url_for("vendor.index"))



@vendor.route("/")
@login_required
def index():
    # check user role for vendor
    if current_user.role.name == "vendor":
        elements = {
            "title": "Welcome",
            "market_name": os.environ["MARKET_NAME"],
        }
        return render_template("vendor_index.html", elements=elements)
    # customer redirect to market
    elif current_user.role.name == "customer":
        return redirect(url_for('market.index'))
    else:
        return redirect(url_for('public.index'))


@vendor.route("/listings")
def listings():
    return render_template("listings.html")
