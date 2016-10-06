from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from agenda.model import IMAGE_FORMATS


class FormWithPic(FlaskForm):
    pic = FileField('pic', validators=[FileAllowed(list(IMAGE_FORMATS.keys()),
                                                   'Images only!')])
    

class UserForm(FormWithPic):
    id = HiddenField('id')
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name')
    contact = StringField('contact')
    presentation = TextAreaField('presentation')
