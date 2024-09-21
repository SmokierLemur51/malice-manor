from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField, 
    StringField, 
    SubmitField,
    TextAreaField, 
)
from wtforms.validators import (
    DataRequired,
    Length,
)


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


class NewVendorSetup(FlaskForm):
    seed_acknowledgment = BooleanField(label='I have saved my seed phrase.', validators=[
        DataRequired(message="Your account will not be recoverable without your seed phrase.")])
    withdrawl_pin = StringField(label='Withdraw Pin', validators=[
        DataRequired(message='Please enter a 6-10 digit pin.'), Length(min=6, max=10)])
    withdrawl_match = StringField(label='Withdraw Pin', validators=[
        DataRequired(message='Please enter a 6-10 digit pin.'), Length(min=6, max=10)])
    submit = SubmitField(label='Finish Venor Registration')