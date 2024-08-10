import os

from flask import Blueprint, flash,redirect, render_template, url_for, request, current_app
from flask_login import current_user, login_required

# from . import forms, queries 


forum = Blueprint('forum', __name__, template_folder="templates/forum", url_prefix="/forum")


@forum.route("/")
@login_required
def index():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("index.html", elements=elements)


@forum.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    return render_template("create_post.html")

