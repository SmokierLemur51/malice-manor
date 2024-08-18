from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired



class CreatePostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    body = TextAreaField(label='Body', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdatePostForm(FlaskForm):
    pass


class CreateCommentForm(FlaskForm):
    comment = StringField(label="Body")


class UpdateCommentForm(FlaskForm):
    pass


