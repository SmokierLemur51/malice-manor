import os
import uuid

from flask import Blueprint, redirect, render_template, url_for, request, current_app
from flask_login import current_user, login_required

from . import forms, queries
from ...models.models import db, Listing, ListingDraft, Vendor


vendor = Blueprint('vendor', __name__, template_folder="templates/vendor", url_prefix="/vendors")


# make sure all authenticated users are vendors
@vendor.before_request
def check_vendor():
    if current_user.is_authenticated:
        if current_user.role.name != 'vendor':
            return redirect('/invalid-request')


# checking to see if before_request works ...
@vendor.route('/test')
@login_required
def test():
    return "Failed"


@vendor.route("/")
@login_required
def index(): 
    elements = {
        'title': f'Your Market | {current_user.public_username}',
    }
    return render_template('vendor_home.html', elements=elements)



"""
There is an issue here in the category/sub category of creating the listing.

We cannot expect the user/vendor to know exactly what categories and sub categories are in 
relation to eachother, and without javascript we cannot make it easier on the user by only 
populatig the sub categories that coincide with their category selection. 

I will do some more thinking, but for now I think the best option is to add a new database
table for ListingDrafts. Making function 'create_listing' step one of a two step process. 

Step one:
    Name it, choose a category, and provide info.  
"""
@vendor.route("/create-listing-draft", methods=['GET', 'POST'])
@login_required
def create_listing_draft():
    elements = {}
    f = forms.CreateListingForm()
    f.category.choices = queries.select_categories(db)
    if f.validate_on_submit():
        # create listing, redirect to market listing ...
        try:   
            draft = ListingDraft( 
                uuid=uuid.uuid4(), # remember, uuid4() is the only truly random generator 
                vendor_id=current_user.id,
                category_id=f.category.data,
                name=f.name.data,
                info=f.info.data,
            )
            db.session.add(draft)
            db.session.commit()
            # redirect user to finalize listing 
            return redirect(url_for("vendor.finalize_listing", uuid=draft.uuid))
        except Exception as e:
            db.session.rollback()
            print(e)
        return redirect(url_for("/listing"))
    return render_template("create_listing.html")


@vendor.route("/finalize-listing/<string:uuid>", methods=["GET", "POST"])
@login_required
def finalize_listing(uuid):
    draft = queries.select_draft(db, uuid)
    if draft is None:
        abort(404)
    elements = {}
    f = forms.FinalizeListingForm()
    # existing values
    f.name.data = draft.name
    f.subcategories.choices = queries.select_categories_sub_categories(db, draft.category.id)
    if f.validate_on_submit():
        l = Listing(
            
        )
        try:
            db.session.add(l)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        return redirect(url_for(''))
    return render_template('finalize_listing.html')


# @vendor.route("/listings")

# @vendor.route("/orders")

# @vendor.route("/history")

# see customer orders, set up special pricing plans, manage relationships
# @vendor.route("/crm")
