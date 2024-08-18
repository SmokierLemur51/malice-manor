import os

from flask import Blueprint, flash,redirect, render_template, url_for, request, current_app
from flask_login import current_user, login_required

from . import forms, queries 
from ...models.models import ForumPost


forum = Blueprint('forum', __name__, template_folder="templates/forum", url_prefix="/forum")


@forum.route("/")
@login_required
def feed():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("feed.html", elements=elements)


@forum.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    # is 'if current_user.is_authenticated' needed here? 
    elements = {
        'title': 'Create Forum Post',
        'market_name': os.environ['MARKET_NAME'],
    }
    _form = forms.CreatePostForm()
    if _form.validate_on_submit():
        post = ForumPost(
            author_id=current_user.id,
            title=_form.title.data,
            body=_form.body.data,
        )
        db.session.add(post)
        db.session.commit()
    return render_template("create_post.html", form=_form, elements=elements)


