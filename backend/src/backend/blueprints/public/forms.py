from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


# It may be best to be authenticated to fill out this form.
class MarketReviewForm(FlaskForm):
    pass
