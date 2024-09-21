import os
import uuid

from flask import Blueprint, redirect, render_template, url_for, request, current_app
from flask_login import current_user, login_required

from . import forms, queries
from ...models.models import db, Listing, ListingDraft, Vendor


vendor = Blueprint('vendor', __name__, template_folder="templates/vendor", url_prefix="/vendors")


@vendor.before_request
def check_vendor():
    """Make sure all authenticated users are actually vendor roles."""
    if current_user.is_authenticated:
        if current_user.role.name != 'vendor':
            return redirect('/invalid-request')


@vendor.before_request
def check_approval():
    """If the Vendor instance does not exist in the database, send to setup page."""
    if current_user.vendor.setup is False:
        return redirect(url_for("vendor.setup_account"))
    

@vendor.route("/new-vendor-setup", methods=['GET', 'POST'])
@login_required
def setup_account():
    """After creation, during the first visit, the vendor will 
    be sent here for information to be presented.

    We will generate a pin on, and only on, their 
    first request to this page. They will then provide us a 
    6-10 digit pin code to be used on withdrawls. A box must
    also be checked signaling they have their recovery phrase 
    and pin saved, those are the only way an account can be 
    updated or recovered. 
    """
    if current_user.is_authenticated and current_user.role.name == "vendor":
        elements = {
            'title': "Vendor Setup | {}".format(current_user.public_username),
            'market_name': os.environ['MARKET_NAME'],
        }
        seed_phrase = seed.generate_seed_phrase(seed.word_list)
        f = forms.NewVendorSetup()
        if f.validate_on_submit(): # can pin comparison go here ??
            if f.withdrawl_pin.data == f.withdrawl_match.data:
                try:
                    db.session.add(Vendor(
                        user_id=current_user.id,
                        recovery_hash=fbcrypt.generate_password_hash(seed_phrase),
                        withdrawl_pin=fbcrypt.generate_password_hash(f.withdrawl_pin.data),
                    ))            
                    db.session.commit()
                    # Successful creation of Vendor, send user to vendor welcome page.
                    return redirect(url_for('vendor.welcome'))
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    # There was an exception with creating the vendor object, reload the page.
                    return render_template("new_vendor_setup.html", form=f)
            else:
                flash("Pin provided must match.")
                # User is authenticated, form has been validated, but pins provided do not match.
                return render_template("new_vendor_setup.html", form=f)
        # If user is authenticated, and the NewVendorSetup form has not been validated
        return render_template("new_vendor_setup.html", form=f)
    else:
        return redirect('/invalid-request')


@vendor.route("/welcome")
@login_required
def vendor_welcome():
    """Intended for vendors on their first visit after creation, or for returning vendors
    to read about some of the tools we have built for them.
    """
    return "Welcome"


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
            category_id=draft.category_id,
            sub_category_id=f.subcategory.data,
            vendor_id=current_user.id,
            name=f.name.data,
            info=f.info.data,
            selling=f.selling.data,
            uuid=uuid.uuid4(),
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
