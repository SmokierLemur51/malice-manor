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
from ...models.models import db, User

users = Blueprint('users', __name__, template_folder="templates/users")

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_athenticated:
        return redirect(url_for("users.invalid_request_credentials"))
    f = forms.RegisterUserForm()
    if f.validate_on_submit():
        # Check usernames are not taken
        pass
    return render_template('register.html', form=f)






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
            # if u.role.
            return redirect(next or url_for('portal.home'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template("login.html", elements=elements, form=f)



# Route to redirect users who try and access an area 
# they do not have permission for.
# Ex: customers requesting vendor routes
@users.route('/invalid-request')
def invalid_request_credentials():
    if current_user.is_athenticated:
        if current_user.role.name == "vendor":
            return redirect(url_for("vendors.home"))
        elif current_user.role.name == "customer":
            return redirect(url_for("market.index"))
        else:
            return redirect(url_for("public.index"))
    else:
        return redirect(url_for("public.index"))


@users.route('/new-vendor', methods=['GET', 'POST'])
def new_vendor():
    # more vendor registration process 
    return render_template()