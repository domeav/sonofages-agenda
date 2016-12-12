#!/usr/bin/env python
from instance import settings
from agenda.model import reset, User, Venue, Tag, Event, EventTag, Occurrence
import random, names
from loremipsum import get_paragraph, get_sentences, get_sentence
from datetime import datetime, timedelta
import os


settings.db.connect()
reset()

IMAGES_FOLDER = 'populate-images'


def generate_mail(name):
    return "{}@{}.com".format(*name.split(' ')[:2])


def generate_presentation():
    return random.choice([get_paragraph(), ''.join(get_sentences(2)), ''])

def generate_venue_name():
    return '{} {}'.format(names.get_full_name(),
                          random.choice(['café',
                                         'concert hall',
                                         'bar',
                                         'restaurant',
                                         'barn',
                                         'house',
                                         'bedroom',
                                         'cantina',
                                         'office',
                                         'basement']))

def generate_address():
    return '''{}, {} street\r{}0 {}Town'''.format(random.randint(1, 227),
                                                  names.get_full_name(),
                                                  random.randint(1000, 9999),
                                                  names.get_full_name().replace(' ', ''))


def set_image(entity, probability):
    if probability < random.random():
        return
    imagename = random.choice(os.listdir(IMAGES_FOLDER))
    entity.set_image(os.path.join(IMAGES_FOLDER, imagename), imagename)

dom = User(name='Dominique Eav',
           email='dom.eav@gmail.com',
           password='password')
dom.save()
users = [dom]
for i in range(15):
    name = names.get_full_name()
    user = User(name=name,
                password=name,
                email=generate_mail(name),
                presentation=generate_presentation())
    set_image(user, 0.5)
    user.save()
    users.append(user)

venues = []
for i in range(20):
    venue = Venue(name=generate_venue_name(),
                  address=generate_address(),
                  contact=generate_mail(names.get_full_name()),
                  description=generate_presentation())
    set_image(venue, 0.6)
    venue.save()
    venues.append(venue)

tags = []
for i in range(15):
    try:
        tag = Tag(name=names.get_last_name())
        set_image(tag, 1)
        tag.save()
        tags.append(tag)
    except:
        pass

events = []
for i in range(100):
    event = Event(title=get_sentence(),
                  description=generate_presentation(),
                  contact=generate_mail(names.get_full_name()),
                  owner=random.choice(users),
                  creation=datetime.now() - timedelta(days=random.randint(1, 365)))
    set_image(event, 0.8)
    event.save()
    etags = []
    for j in range(random.randint(0, 3)):
        tag = random.choice(tags)
        if tag in etags:
            continue
        eventtag = EventTag(event=event, tag=tag)
        eventtag.save()
        etags.append(tag)
    for j in range(random.choice([1, 1, 1, 1, 2, 3, 5])):
        start = datetime.now() + timedelta(hours=random.randint(0, 90*24))
        occurrence = Occurrence(event=event,
                               start=start,
                               end=start+timedelta(hours=random.randint(1, 5)),)
        if random.randint(0, 5) != 0:
            occurrence.venue = random.choice(venues)
        occurrence.save()

