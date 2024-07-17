import os

from flask import Blueprint, redirect, render_template, url_for, request, current_app

from ...models.models import db, Vendor
# from ...models import 

# from .forms import 


vendor = Blueprint('vendor', __name__, template_folder="templates/vendor", url_prefix="/vendors")


@vendor.route("/populate")
def populate():
    from .populate import populate_vendors
    populate_vendors(db)
    return redirect(url_for("vendor.index"))


@vendor.route("/login", methods=["GET", "POST"])
def login():
    return 


@vendor.route("/")
def index():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }

    return render_template("vendor_index.html", elements=elements)


@vendor.route("/listings")
def listings():
    return render_template("listings.html")
