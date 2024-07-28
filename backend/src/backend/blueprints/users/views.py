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
from ...models.models import db

users = Blueprint('users', __name__, template_folder="templates/users")

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_athenticated:
        return redirect(url_for("market"))
    form = forms.RegisterUserForm()
