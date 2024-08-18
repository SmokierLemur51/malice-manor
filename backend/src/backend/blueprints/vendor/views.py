import os

from flask import Blueprint, redirect, render_template, url_for, request, current_app
from flask_login import current_user, login_required

from ...models.models import db, Vendor


vendor = Blueprint('vendor', __name__, template_folder="templates/vendor", url_prefix="/vendors")


@vendor.route("/populate")
def populate():
    from .populate import populate_vendors
    populate_vendors(db)
    return redirect(url_for("vendor.home"))



@vendor.route("/")
@login_required
def home():
    if current_user.role.name != "vendor":
        # send user to appropriate area via users.redirect_user
        return redirect('/invalid-request') 
    else:
        elements = {
            'title': f'Your Market | {current_user.public_username}',
        }
        return render_template('vendor_home.html', elements=elements)


@vendor.route("/create-listing", methods=['GET', 'POST'])
@login_required
def create_listing():
    return render_template("create_listing.html")


# @vendor.route("/listings")

# @vendor.route("/orders")

# @vendor.route("/history")

# @vendor.route("/crm")