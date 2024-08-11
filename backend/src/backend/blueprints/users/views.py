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
from ...toolbox.helpers import generate_secret_key


users = Blueprint('users', __name__, template_folder="templates/users")


@users.route('/login', methods=['GET', 'POST'])
def login():
    # redirect to the portal homepage if authenticated
    if current_user.is_authenticated:
        return redirect(url_for('portal.home'))
    # login page information
    elements = {"title": "Login"}
    f = forms.LoginForm()
    if f.validate_on_submit():
        u = queries.get_user(db, f.username.data)
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
    return redirect(url_for('portal.login'))


# Route to redirect users who try and access an area they do not have permission for.
# Ex: customers requesting vendor routes
# Also used after login to prevent redundant code. 
@users.route('/invalid-request')
@users.route('/redirect-user')
@login_required
def redirect_user():
    if current_user.is_authenticated:
        if current_user.role.name == "admin":
            return redirect(url_for('admin.home'))
        elif current_user.role.name == "vendor":
            return redirect(url_for('vendors.home'))
        else:
            return redirect(url_for('market.index'))
    else:
        return redirect(url_for('public.index'))
        

# Register customer
@users.route("/register-customer", methods=["GET", "POST"])
def register_customer():
    elements = {"title": "Register Market Account"}
    form = forms.RegisterUserForm()
    if form.validate_on_submit():
        if form.password.data == form.password_match.data: # and queries.check_unique_usernames(db, form.public_username.data, form.private_username.data)
            u = User(
                role_id=queries.load_role(db, "customer").id,
                public_username=form.public_username.data,
                private_username=form.private_username.data,
                password=fbcrypt.generate_password_hash(form.password.data),
                secret_key=generate_secret_key(),
            )
            with current_app.app_context():    
                with db.session.begin():
                    try:
                        db.session.add(u)
                        db.session.flush()
                        # new customer
                        c = Customer(user_id=u.id)
                        db.session.add(c)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(e)
            return redirect(url_for("users.login"))
        else:
            flash("Passwords must match.")
            return render_template("register_customer.html", elements=elements, form=form)
    return render_template("register_customer.html")


# New vendors 
@users.route("/register-vendor", methods=["GET", "POST"])
def register_vendor():
    elements = {"title": "Register Vendor Account"}
    form = forms.RegisterUserForm()
    if form.validate_on_submit():
        if form.password.data == form.password_match.data:
            u = User(
                role_id=queries.load_role(db, "vendor").id,
                public_username=form.public_username.data,
                private_username=form.private_username.data,
                password=fbcrypt.generate_password_hash(form.password.data),
                secret_key=generate_secret_key(),
            )
            with current_app.app_context():    
                with db.session.begin():
                    try:
                        db.session.add(u)
                        db.session.flush()
                        # new vendor
                        v = Vendor(user_id=u.id)
                        db.session.add(v)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(e)
            return redirect(url_for("users.login"))
        else:
            flash("Passwords must match.")
            return render_template("register_vendor.html", elements=elements, form=form)
    return render_template("register_vendor.html", elements=elements, form=form)


@users.route('/test/<string:priv>/<string:pub>')
def test(priv, pub):
    if queries.check_unique_usernames(db, priv, pub):
        return "True"
    else:
        return "False"


@users.route('/create-users')
def create_users():
    
    users = [
        User()
    ]