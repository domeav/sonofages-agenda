from agenda.model import Occurrence, Event
from agenda.forms import EventForm
from flask import render_template, request, redirect, url_for
from datetime import datetime
from agenda import app


@app.route('/')
@app.route('/agenda/')
@app.route('/agenda/events/')
def events():
    page = request.args.get('p', 1)
    target_date = request.args.get('d', datetime.now())
    occurrences = Occurrence.select()\
                            .where(Occurrence.start >= target_date)\
                            .order_by(Occurrence.start).paginate(page, 100)
    return render_template('agenda.html', occurrences=occurrences)


@app.route('/agenda/event/<occurrence_id>')
def event(occurrence_id):
    occurrence = Occurrence.get(Occurrence.id == occurrence_id)
    return render_template('event.html', occ=occurrence)


@app.route('/agenda/meta_event/<event_id>')
def meta_event(event_id):
    event = Event.get(Event.id == event_id)
    return render_template('meta_event.html', event=event)


@app.route('/agenda/meta_event/edit/<event_id>')
@app.route('/agenda/meta_event/edit/')
def edit_event(event_id=None):
    event = None
    if event_id:
        event = Event.get(Event.id == event_id)    
    return render_template('event_edit.html', form=EventForm(obj=event))


@app.route('/agenda/meta_event/save/', methods=['POST'])
def save_event():
    form = EventForm()
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
    # TODO: owner
    event.save()
    return redirect(url_for('meta_event', event_id=event.id))
