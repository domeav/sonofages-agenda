from agenda.model import Occurrence, User, Event
from flask import Flask, render_template, request
from flask_security import PeeweeUserDatastore, Security
from flask_mail import Mail
from datetime import datetime
from instance import settings
import locale

locale.setlocale(locale.LC_ALL, settings.LOCALE)

app = Flask(__name__)

from agenda.model import User, Role, UserRole
user_datastore = PeeweeUserDatastore(settings.db, User, Role, UserRole)
security = Security(app, user_datastore)

app.config['MAIL_SERVER'] = settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
app.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
mail = Mail(app)

@app.context_processor
def inject():
    return dict(site_title=settings.SITE_TITLE)

import agenda.events
import agenda.users
import agenda.pics
import agenda.venues
import agenda.tags

