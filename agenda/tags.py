from agenda.model import Tag, Event, EventTag, Occurrence
from agenda.forms import TagForm
from flask import render_template, request, redirect, url_for
from agenda import app


@app.route('/agenda/tag/<tag_id>')
def tag(tag_id):
    tag = Tag.get(Tag.id == tag_id)
    return render_template('tag.html', tag=tag)


@app.route('/agenda/tags/')
def tags():
    tags = Tag.select().order_by(Tag.name)
    return render_template('tags.html', tags=tags)


@app.route('/agenda/tag_events/<tag_id>')
def tag_events(tag_id):
    occurrences = Occurrence.select()\
                  .join(Event)\
                  .join(EventTag)\
                  .where(EventTag.tag == tag_id)\
                  .order_by(Occurrence.start).desc()
    return render_template('tag_events.html', occurrences=occurrences)


@app.route('/agenda/tag/edit/<tag_id>')
@app.route('/agenda/tag/edit/')
def edit_tag(tag_id=None):
    tag = None
    if tag_id:
        tag = Tag.get(Tag.id == tag_id)    
    return render_template('tag_edit.html', form=TagForm(obj=tag))


@app.route('/agenda/tag/save/', methods=['POST'])
def save_tag():
    form = TagForm()
    if not form.validate_on_submit():
        return render_template('tag_edit.html', form=form)
    if form.id.data:
        tag = Tag.get(Tag.id == form.id.data)
    else:
        tag = Tag()
    tag.name = form.name.data
    tag.set_image(form.pic.data, form.pic.data.filename)
    tag.save()
    return redirect(url_for('tag', tag_id=tag.id))

            
    
