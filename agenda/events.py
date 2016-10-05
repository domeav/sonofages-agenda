from agenda.model import Occurrence, Event
from flask import render_template, request
from datetime import datetime
from agenda import app


@app.route('/agenda/')
def agenda():
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
