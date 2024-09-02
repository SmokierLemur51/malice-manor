from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired

class CreateListingForm(FlaskForm):
    name = StringField(label='Listing Name', validators=[
        DataRequired(message='Please provide listing name.')])
    # Category and Sub Categories provided in view function.
    category = SelectField('Category', validators=[
        DataRequired(message='Please select a category.')])
    subcategory = SelectField('Sub Category', validators=[
        DataRequired(message='Please select a category.')])
    info = TextAreaField(label='Listing Information', validators=[
        DataRequired(message='Information about your listing is required.')])
    # Selling price will be converted from Galleons, Sickles and Knuts ... 
    selling = IntegerField(label='Selling Price', validators=[
        DataRequired(message='Please provide selling price.')])


class CreateListingDraftForm(FlaskForm):
    name = StringField(label='Listing Name', validators=[
        DataRequired(message='Please provide listing name.')])
    # Category and Sub Categories provided in view function.
    category = SelectField('Category', validators=[
        DataRequired(message='Please select a category.')]) 
    info = TextAreaField(label='Listing Information', validators=[
        DataRequired(message='Information about your listing is required.')])


class FinalizeListingForm(FlaskForm):
    name = StringField(label='Listing Name', validators=[
        DataRequired(message='Please provide listing name.')])
    # Category and Sub Categories provided in view function.
    subcategory = SelectField('Sub Category', validators=[
        DataRequired(message='Please select a sub category.')]) 
    info = TextAreaField(label='Listing Information', validators=[
        DataRequired(message='Information about your listing is required.')])


