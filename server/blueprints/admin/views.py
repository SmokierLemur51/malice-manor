import os

from flask import Blueprint, redirect, render_template, url_for, request, current_app

from ...models.models import db, Vendor, Customer
# from ...models import 

# from .forms import 


admin = Blueprint('admin', __name__, template_folder="templates/admin", url_prefix="/admin")


@admin.route("/")
def index():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("index.html", elements=elements)



@admin.route("/vendors")
def vendors():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
        "vendors": db.session.scalars(db.select(Vendor)).all(),
    }
    return render_template("vendors.html", elements=elements)




@admin.route("/customers")
def customers():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
        "customers": db.session.scalars(db.select(Customer)).all(),
    }
    return render_template("customers.html", elements=elements)




@admin.route("/orders")
def orders():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
        # "orders": db.session.scalars(db.select(Order)).all(),
    }
    return render_template("orders.html", elements=elements)




@admin.route("/escrow")
def escrow():
    elements = {
        "title": "Welcome Team",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("escrow.html", elements=elements)

