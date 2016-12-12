from agenda.model import User, Event
from agenda.forms import UserForm
from flask import render_template, request, redirect, url_for
from agenda import app


@app.route('/user/<user_id>')
def user(user_id):
    user = User.get(User.id == user_id)
    return render_template('user.html', user=user)


@app.route('/users/')
def users():
    users = User.select().order_by(User.username)
    return render_template('users.html', users=users)


@app.route('/user_events/<user_id>')
def user_events(user_id):
    events = Event.select()\
                  .where(Event.owner == user_id)\
                  .order_by(Event.creation).desc()
    return render_template('user_events.html', events=events)


@app.route('/user/edit/<user_id>')
@app.route('/user/edit/')
def edit_user(user_id=None):
    user = None
    if user_id:
        user = User.get(User.id == user_id)    
    return render_template('user_edit.html', form=UserForm(obj=user))


@app.route('/user/save/', methods=['POST'])
def save_user():
    form = UserForm()
    if not form.validate_on_submit():
        return render_template('user_edit.html', form=form)
    if form.id.data:
        user = User.get(User.id == form.id.data)
    else:
        user = User()
    user.username = form.username.data
    user.name = form.name.data
    user.contact = form.contact.data
    user.presentation = form.presentation.data
    user.set_image(form.pic.data, form.pic.data.filename)
    user.save()
    return redirect(url_for('user', user_id=user.id))

            
    
