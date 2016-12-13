from agenda.model import Occurrence, Event, Venue, Tag, EventTag
from agenda.forms import EventForm
from flask import render_template, request, redirect, url_for
from flask_security import login_required
from datetime import datetime
from agenda import app

@app.route('/')
@app.route('/events/')
def events():
    page = request.args.get('p', 1)
    target_date = request.args.get('d', datetime.now())
    occurrences = Occurrence.select()\
                            .where(Occurrence.start >= target_date)\
                            .paginate(page, 30)
    return render_template('agenda.html', occurrences=occurrences)


@app.route('/event/<occurrence_id>')
def event(occurrence_id):
    occurrence = Occurrence.get(Occurrence.id == occurrence_id)
    return render_template('event.html', occ=occurrence)


@app.route('/meta_event/<event_id>')
def meta_event(event_id):
    event = Event.get(Event.id == event_id)
    return render_template('meta_event.html', event=event)


@app.route('/meta_event/edit/<event_id>')
@app.route('/meta_event/edit/')
def edit_event(event_id=None):
    event = None
    if event_id:
        event = Event.get(Event.id == event_id)
    form = EventForm(obj=event)
    form.set_venues(Venue.select())
    return render_template('event_edit.html', form=form,
                           tags=Tag.select(),
                           eventtags={et.tag.id for et in event.eventtags})


@app.route('/meta_event/save/', methods=['POST'])
def save_event():
    form = EventForm()
    form.set_venues(Venue.select())
    if not form.validate_on_submit():
        return render_template('event_edit.html', form=form)
    if form.id.data:
        event = Event.get(Event.id == form.id.data)
    else:
        event = Event()
    event.title = form.title.data
    event.contact = form.contact.data
    event.description = form.description.data
    if not event.creation:
        event.creation = datetime.now()
    event.set_image(form.pic.data, form.pic.data.filename)
    event.save()
    for entry in form.occurrences.entries:
        if entry.data['id']:
            occurrence = Occurrence.get(Occurrence.id == entry.data['id'])
        else:
            occurrence = Occurrence()
        occurrence.start = entry.data['start']
        occurrence.end = entry.data['end']
        occurrence.event = event
        
        if entry.data['venue_id'] != 0:            
            occurrence.venue_id = entry.data['venue_id']
        else:
            occurrence.venue_id = None
        occurrence.save()
        if entry.data['delete_gig']:        
            occurrence.delete_instance()
    existing_tags = { et.tag_id: et for et in event.eventtags }
    for key, value in request.form.items():
        if key.startswith('tag-'):
            tag_id = int(value)
            if tag_id not in existing_tags:
                et = EventTag(event=event, tag_id=tag_id)
                et.save()
            else:
                del(existing_tags[tag_id])
    for key, value in existing_tags.items():
        value.delete_instance()
    return redirect(url_for('meta_event', event_id=event.id))
