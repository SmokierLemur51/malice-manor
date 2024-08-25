from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import EmailField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

from ...models.models import ForumCommunity

class CreateCommunityForm(FlaskForm):
    name = StringField(label='New Community Name', validators=[DataRequired()])
    description = TextAreaField(label='Community Purpose')
    submit = SubmitField('Create Community')



class CreatePostForm(FlaskForm):
    # Community field is not neccesary, for now it is best handled in the route.
    title = StringField(label='Title', validators=[DataRequired()])
    body = TextAreaField(label='Body', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdatePostForm(FlaskForm):
    pass


class CreateCommentForm(FlaskForm):
    comment = StringField(label="Body")


class UpdateCommentForm(FlaskForm):
    pass


