import os

from quart import Blueprint, redirect, render_template, url_for, request, current_app

admin = Blueprint('admin', __name__, template_folder="templates/admin", url_prefix="/admin")


@admin.route("/test/populate")
async def populate_view():
    return redirect(url_for('admin.index'))


@admin.route("/")
async def index():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
    }
    return await render_template("admin_index.html", elements=elements)


@admin.route("/vendors")
async def vendors():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
    }
    return await render_template("admin_vendors.html", elements=elements)


@admin.route("/customers")
async def customers():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
    }
    return await render_template("admin_customers.html", elements=elements)


@admin.route("/orders")
async def orders():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
    }
    return await render_template("orders.html", elements=elements)


@admin.route("/escrow")
async def escrow():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
    }
    return await render_template("escrow.html", elements=elements)

