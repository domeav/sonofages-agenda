from peewee import *
from werkzeug.utils import secure_filename
from PIL import Image
import io


db = SqliteDatabase('agenda.db')


IMAGE_FORMATS = {'jpg': 'jpeg',
                 'jpeg': 'jpeg',
                 'png': 'png'}

class BaseModel(Model):
    class Meta:
        database = db

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
        
        
class User(ModelWithPic):
    username = CharField(unique=True)
    name = CharField(null=True)    
    contact = CharField(index=True, null=True)
    presentation = TextField(null=True)
        
    
class Venue(ModelWithPic):
    name = CharField(index=True)
    address = TextField(index=True)
    contact = CharField(index=True, null=True)
    description = TextField(null=True)
    pic = BlobField(null=True)
    thumb = BlobField(null=True)

    
class Tag(ModelWithPic):
    name = CharField(unique=True)    
    

class Event(ModelWithPic):
    title = CharField(index=True)
    description = TextField(null=True)
    contact = CharField(null=True)
    creation = DateTimeField()
    owner = ForeignKeyField(User)
    

class EventTag(BaseModel):
    event = ForeignKeyField(Event, related_name="eventtags")
    tag = ForeignKeyField(Tag)
    
    
class Occurrence(BaseModel):
    event = ForeignKeyField(Event, related_name='occurrences')
    venue = ForeignKeyField(Venue, null=True)
    start = DateTimeField()
    end = DateTimeField(null=True)


def reset():
    all = [User, Venue, Tag, Event, EventTag, Occurrence]
    db.drop_tables(all)
    db.create_tables(all)
    

if __name__ == '__main__':
    db.connect()
    reset()
