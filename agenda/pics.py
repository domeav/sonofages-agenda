from agenda.model import User, Event, Venue, Tag
from flask import abort, send_file
from agenda import app
import io

ENTITY_TYPES = {'user': User,
                'venue': Venue,
                'event': Event,
                'tag': Tag}

@app.route('/thumb/<entity_type>/<entity_id>.<ext>', defaults={'thumb': True})
@app.route('/pic/<entity_type>/<entity_id>.<ext>', defaults={'thumb': False})
def image(entity_type, entity_id, ext, thumb):
    entity = ENTITY_TYPES[entity_type]
    record = entity.get(entity.id == entity_id)
    image = record.thumb if thumb else record.pic
    return send_file(io.BytesIO(image),
                     attachment_filename='{}.{}'.format(entity_id, ext),
                     mimetype='image/{}'.format(ext))


