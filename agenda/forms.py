from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    id = HiddenField('id')
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name')
    contact = StringField('contact')
    presentation = TextAreaField('presentation')
