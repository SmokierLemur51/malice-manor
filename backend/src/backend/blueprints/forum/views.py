import os
import uuid

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
from ...models.models import db, ForumCommunity, ForumPost, PostComment
from ...toolbox import conversions


forum = Blueprint('forum', __name__, template_folder="templates/forum", url_prefix="/forum")


@forum.route("/")
@login_required
def feed():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    c = queries.select_communities(db)
    return render_template("feed.html", elements=elements, communities=c)


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
            return render_template(
                'create_community.html',
                form=f, 
                elements=elements,
            )
    return render_template(
        'create_community.html', 
        form=f,
        elements=elements)


@forum.route('/c/<string:community>', methods=['GET'])
@login_required
def community_feed(community):
    c = queries.select_community(db, community)
    if c is None:
        # Final version should redirec to page specifically for this err
        # ex: redirect(url_for('forum.create_community')) 
        abort(404)
    else :
        return render_template(
            'community_feed.html', 
            elements={'title': c.name},
            posts=queries.select_posts(db, c, 'all', None))


@forum.route("/c/<string:community>/create-post", methods=['GET', 'POST'])
@login_required
def create_post(community):
    c = queries.select_community(db, community)
    if c is None:
        # Final version should redirec to page specifically for this err
        # ex: redirect(url_for('forum.create_community')) 
        abort(404)
    else :
        f = forms.CreatePostForm()
        if f.validate_on_submit():
            post = ForumPost(
                author_id=current_user.id,
                community_id=c.id,
                title=f.title.data,
                body=f.body.data,
                slug=conversions.convert_into_slug(f.title.data),
                token=uuid.uuid4(), # uui4() generates random uuid instead of using device info to generate
            )
            db.session.add(post)
            db.session.commit()
            return redirect(
                url_for(
                    'forum.view_post', 
                    token=post.token,
                    post_slug=post.slug))
        return render_template(
            "create_post.html", 
            form=f, 
            elements={
                'title': 'Create Forum Post',
                'market_name': os.environ['MARKET_NAME'],
            })


@forum.route("/c/")

@forum.route('/c/<string:community>/<string:token>/<string:post_slug>', methods=['GET'])
@login_required
def view_post(community):
    c = queries.select_community(db, community)
    if c is None:
        # Final version should redirec to page specifically for this err
        # ex: redirect(url_for('forum.create_community')) 
        abort(404)
    p = queries.select_post(db, token, slug)
    if p is None:
        # Final version should redirec to page specifically for this err
        # ex: redirect(url_for('forum.create_community')) 
        abort(404)
    f = CreatePostCommentForm()
    if f.validate_on_submit():
        comment = PostComment(
            author_id=current_user.id,
            post_id=p.id,
            comment=f.comment.data)
        try:
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            print(e)
        # Refresh page with comment showing
        return render_template(
            'community_post.html',
            post=p,
            elements={'title': c.name}
        )
    else:
        return render_template(
            'community_post.html',
            post=p, 
            elements={'title': c.name})

