import os

from flask import Blueprint, flash,redirect, render_template, url_for, request, current_app
from flask_login import current_user

from ...models.models import db


public = Blueprint('public', __name__, template_folder="templates/public", url_prefix="/")


@public.route("/")
def index():
    if current_user.is_authenticated:
        return redirect("/redirect-user")
    # query latest info
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("index.html", elements=elements)

