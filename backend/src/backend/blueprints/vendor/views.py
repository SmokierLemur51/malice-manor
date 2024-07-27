import os

from quart import Blueprint, redirect, render_template, url_for, request, current_app


vendor = Blueprint('vendor', __name__, template_folder="templates/vendor", url_prefix="/vendors")


@vendor.route("/populate")
async def populate():
    from . import populate as pop 
    await pop.populate_vendors()
    return redirect(url_for("vendor.index"))


@vendor.route("/login", methods=["GET", "POST"])
async def login():
    return await render_template("login.html")


@vendor.route("/")
async def index():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }

    return await render_template("vendor_index.html", elements=elements)


@vendor.route("/listings")
async def listings():
    return await render_template("listings.html")
