from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired



class RegisterUserForm(FlaskForm):
    public_username = StringField(label='Public Username', validators=[DataRequired()])
    private_username = StringField(label='Private Username', validators=[DataRequired()])
    password = StringField(label='Password', validators=[DataRequired()])
    password_match = StringField(label='Re-Enter Password', validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class LoginForm(FlaskForm):
    private_username = StringField(label='Private Username', validators=[DataRequired()])
    password = StringField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label="Submit")

