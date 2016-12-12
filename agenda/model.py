from peewee import *
from werkzeug.utils import secure_filename
from flask_security import UserMixin, RoleMixin
from PIL import Image
import io
from instance import settings

IMAGE_FORMATS = {'jpg': 'jpeg',
                 'jpeg': 'jpeg',
                 'png': 'png'}

class BaseModel(Model):
    class Meta:
        database = settings.db

class ModelWithPic(BaseModel):
    pic = BlobField(null=True)
    thumb = BlobField(null=True)
    image_type = CharField(null=True)
    def set_image(self, file, filename):
        if not filename:
            return
        self.image_type = secure_filename(filename).split('.')[-1]
        image = Image.open(file)
        image.thumbnail((800, 800))
        pic = io.BytesIO()
        image.save(pic, format=IMAGE_FORMATS[self.image_type])
        self.pic = pic.getvalue()
        image.thumbnail((128, 128))
        thumb = io.BytesIO()
        image.save(thumb, format=IMAGE_FORMATS[self.image_type])
        self.thumb = thumb.getvalue()
        

class Role(BaseModel, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)

    
class User(ModelWithPic, UserMixin):
    class Meta:
        order_by = ('name',)
    name = TextField()
    email = TextField()
    password = TextField()
    presentation = TextField(null=True)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)

class UserRole(BaseModel):
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)
        
    
class Venue(ModelWithPic):
    class Meta:
        order_by = ('name',)
    name = CharField(index=True)
    address = TextField(index=True)
    contact = CharField(index=True, null=True)
    description = TextField(null=True)
    pic = BlobField(null=True)
    thumb = BlobField(null=True)

    
class Tag(ModelWithPic):
    class Meta:
        order_by = ('name',)
    name = CharField(unique=True)    
    

class Event(ModelWithPic):
    class Meta:
        order_by = ('title',)
    title = CharField(index=True)
    description = TextField(null=True)
    contact = CharField(null=True)
    creation = DateTimeField()
    owner = ForeignKeyField(User)
    

class EventTag(BaseModel):
    event = ForeignKeyField(Event, related_name="eventtags")
    tag = ForeignKeyField(Tag)
    
    
class Occurrence(BaseModel):
    class Meta:
        order_by = ('start',)
    event = ForeignKeyField(Event, related_name='occurrences')
    venue = ForeignKeyField(Venue, null=True)
    start = DateTimeField()
    end = DateTimeField(null=True)


def reset():
    all = [Role, User, UserRole, Venue, Tag, Event, EventTag, Occurrence]
#    settings.db.drop_tables(all)
    settings.db.create_tables(all)
    

if __name__ == '__main__':
    settings.db.connect()
    reset()
