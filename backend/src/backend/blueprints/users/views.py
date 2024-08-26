import os
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from . import forms, queries
from ...extensions import fbcrypt
from ...models.models import db, User
from ...models.queries import load_role
from ...toolbox.helpers import generate_secret_key


users = Blueprint('users', __name__, template_folder="templates/users")


# Route to redirect users who try and access an area they do not have permission for.
# Ex: customers requesting vendor routes
# Also used after login to prevent redundant code. 
@users.route('/invalid-request')
@users.route('/redirect-user')
@login_required
def redirect_user():
    if current_user.is_authenticated:
        if current_user.role.name == "admin":
            return redirect(url_for('admin.home'), code=301)
        elif current_user.role.name == "vendor":
            return redirect(url_for('vendor.home'), code=301)
        else:
            return redirect(url_for('market.index'), code=301)
    else:
        return redirect(url_for('public.index'), code=301)
        

@users.route('/login', methods=['GET', 'POST'])
def login():
    # redirect to the portal homepage if authenticated
    if current_user.is_authenticated:
        return redirect('/redirect-user')
    # login page information
    elements = {
        "title": "Login",
        "market_name": os.environ['MARKET_NAME'],    
    }
    f = forms.LoginForm()
    if f.validate_on_submit():
        u = queries.get_user(db, f.private_username.data)
        print(f"User Pass: {u.password}, Given: {f.password.data}")
        if u and fbcrypt.check_password_hash(u.password, f.password.data):
            login_user(u)
            return redirect('/redirect-user')
        else:
            flash('Invalid credentials.', 'danger')
    return render_template("login.html", elements=elements, form=f)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('public.index'))


# Register customer
@users.route("/register-customer", methods=["GET", "POST"])
def register_customer():
    elements = {
        "title": "Register Market Account",
        "market_name": os.environ['MARKET_NAME'],    
    }
    form = forms.RegisterUserForm()
    if form.validate_on_submit():
        if form.password.data == form.password_match.data: # and queries.check_unique_usernames(db, form.public_username.data, form.private_username.data)
            u = User(
                role_id=load_role(db, "customer").id,
                public_username=form.public_username.data,
                private_username=form.private_username.data,
                password=fbcrypt.generate_password_hash(form.password.data),
                secret_key=generate_secret_key(),
            )
            # Need a try and excpet block here to handle a transaction that has already begun
            # Error: sqlalchemy.exc.InvalidRequestError
            # Do I even need to have a with db.session.begin() here? 
            # Need to clean this up before moving into the forum.
            try:
                db.session.add(u)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            return redirect(url_for("users.login"))
        else:
            flash("Passwords must match.")
            return render_template("register_customer.html", elements=elements, form=form)
    return render_template("register_customer.html", elements=elements, form=form)


# New vendors 
@users.route("/register-vendor", methods=["GET", "POST"])
def register_vendor():
    elements = {
        "title": "Register Vendor Account",
        "market_name": os.environ['MARKET_NAME'],    
    }
    form = forms.RegisterUserForm()
    if form.validate_on_submit():
        if form.password.data == form.password_match.data:
            u = User(
                role_id=load_role(db, "vendor").id,
                public_username=form.public_username.data,
                private_username=form.private_username.data,
                password=fbcrypt.generate_password_hash(form.password.data),
                secret_key=generate_secret_key(),
            )    
            try:
                db.session.add(u)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            return redirect(url_for("users.login"))
        else:
            flash("Passwords must match.")
            return render_template("register_vendor.html", elements=elements, form=form)
    return render_template("register_vendor.html", elements=elements, form=form)



# Post login welcome screen. Show actions available to user.
@users.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')
    
