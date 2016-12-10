from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField, DateTimeField, FieldList, FormField, SelectField, BooleanField, SelectMultipleField, widgets
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from agenda.model import IMAGE_FORMATS


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    
class FormWithPic(FlaskForm):
    pic = FileField('pic', validators=[FileAllowed(list(IMAGE_FORMATS.keys()),
                                                   'Images only!')])
    
class UserForm(FormWithPic):
    id = HiddenField('id')
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name')
    contact = StringField('contact')
    presentation = TextAreaField('presentation')


class VenueForm(FormWithPic):
    id = HiddenField('id')
    name = StringField('name', validators=[DataRequired()])
    address = TextAreaField('address', validators=[DataRequired()])
    contact = StringField('contact')
    description = TextAreaField('description')

class TagForm(FormWithPic):
    id = HiddenField('id')    
    name = StringField('name', validators=[DataRequired()])


class OccurrenceForm(FlaskForm):
    id = HiddenField('id')
    venue_id = SelectField('venue', coerce=int)
    start = DateTimeField('start')
    end = DateTimeField('end')
    delete_gig = BooleanField('delete?')

    
class EventForm(FormWithPic):
    def set_venues(self, venues):
        venues = [(0, '--')] + [(v.id, v.name) for v in venues]
        for occform in self.occurrences:
            occform.venue_id.choices = venues
    id = HiddenField('id')    
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description')
    contact = StringField('contact')
    occurrences = FieldList(FormField(OccurrenceForm), min_entries=1)
    
