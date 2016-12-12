from agenda.model import Venue, Event, Occurrence
from agenda.forms import VenueForm
from flask import render_template, request, redirect, url_for
from agenda import app


@app.route('/venue/<venue_id>')
def venue(venue_id):
    venue = Venue.get(Venue.id == venue_id)
    return render_template('venue.html', venue=venue)


@app.route('/venues/')
def venues():
    venues = Venue.select().order_by(Venue.name)
    return render_template('venues.html', venues=venues)


@app.route('/venue_events/<venue_id>')
def venue_events(venue_id):
    events = Event.select()\
                  .join(Occurrence)\
                  .where(Occurrence.venue == venue_id)\
                  .order_by(Occurrence.start).desc()
    return render_template('venue_events.html', events=events)


@app.route('/venue/edit/<venue_id>')
@app.route('/venue/edit/')
def edit_venue(venue_id=None):
    venue = None
    if venue_id:
        venue = Venue.get(Venue.id == venue_id)    
    return render_template('venue_edit.html', form=VenueForm(obj=venue))


@app.route('/venue/save/', methods=['POST'])
def save_venue():
    form = VenueForm()
    if not form.validate_on_submit():
        return render_template('venue_edit.html', form=form)
    if form.id.data:
        venue = Venue.get(Venue.id == form.id.data)
    else:
        venue = Venue()
    venue.name = form.name.data
    venue.address = form.address.data
    venue.contact = form.contact.data
    venue.description = form.description.data
    venue.set_image(form.pic.data, form.pic.data.filename)
    venue.save()
    return redirect(url_for('venue', venue_id=venue.id))

            
    
