import os

from flask import (
    abort, 
    Blueprint, 
    flash,redirect, 
    render_template, 
    url_for, 
    request, 
    current_app,
)
from flask_login import current_user, login_required

from . import forms, queries 
from ...models.models import db, ForumCommunity, ForumPost


forum = Blueprint('forum', __name__, template_folder="templates/forum", url_prefix="/forum")


@forum.route("/")
@login_required
def feed():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("feed.html", elements=elements)


@forum.route("/create-community", methods=['GET', 'POST'])
@login_required
def create_community():
    elements = {}
    f = forms.CreateCommunityForm()
    if f.validate_on_submit():
        # check unique
        if queries.check_unique(db, f.name.data):
            c = ForumCommunity(
                owner_id=current_user.id,
                name=f.name.data,
                description=f.description.data,
            )
            db.session.add(c)
            db.session.commit()
            return redirect(url_for('forum.community_feed', community=c.name))
        else:
            # community already exists
            flash('That community already exists. Provided name must be unique.')
            return render_template('create_community.html', elements=elements, form=f)
    return render_template('create_community.html', elements=elements, form=f)


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


@forum.route('/c/<string:community>', methods=['GET'])
@login_required
def community_feed(community):
    c = queries.query_community(db, community)
    if c is None:
        # Final version should redirec to page specifically for this err
        # ex: redirect(url_for('forum.create_community')) 
        abort(404)
    else :
        e = {
            'title': c.name,
        }
        return render_template('community_feed.html', elements=e)