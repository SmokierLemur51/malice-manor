import os

from flask import Blueprint, flash,redirect, render_template, url_for, request, current_app
from flask_login import current_user, login_required

from . import forms, queries 
from ...models.models import db, ForumPost


forum = Blueprint('forum', __name__, template_folder="templates/forum", url_prefix="/forum")


@forum.route("/")
@login_required
def feed():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("feed.html", elements=elements)


@forum.route("/<string:community>/create-post", methods=['GET', 'POST'])
@login_required
def create_post(community):
    elements = {
        'title': 'Create Forum Post',
        'market_name': os.environ['MARKET_NAME'],
    }
    f = forms.CreatePostForm()
    if f.validate_on_submit():
        post = ForumPost(
            author_id=current_user.id,
            title=f.title.data,
            body=f.body.data,
        )
        db.session.add(post)
        db.session.commit()
        # # # # # # # # # # 
        # Working here ...
        # Need to create communities (sub-reddits)
        # As well as
        return redirect(url_for())
    return render_template("create_post.html", form=f, elements=elements)


