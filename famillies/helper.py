import time
import random
import datetime

from .models import Surname
from .models import FamillieList
from .models import RelationType

from geopy.geocoders import Nominatim

from django.contrib.gis.geos import Point


# Set age for objects
def set_age(query):
    today = datetime.datetime.today()
    for obj in query:
        born = obj.date
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        obj.age = age

    return query


# Generate view
def generate_family():
    items = Surname.objects.all()
    surname = random.choice(items)

    address = get_random_address()

    father_name = get_random_name('male')
    mother_name = get_random_name('female')

    father = RelationType.objects.get(relation='Батько')
    mother = RelationType.objects.get(relation='Матір')
    daughter = RelationType.objects.get(relation='Донька')
    son = RelationType.objects.get(relation='Син')

    mother_date = random_date("1960-1-1", "1981-12-31", random.random())
    father_date = random_date("1960-1-1", "1981-12-31", random.random())

    FamillieList.objects.create(
        name=father_name,
        surname=surname,
        relation=father,
        date=father_date,
        address=address,
        point=Point(x=address.latitude, y=address.longitude)
    )

    FamillieList.objects.create(
        name=mother_name,
        surname=surname,
        relation=mother,
        date=mother_date,
        address=address,
        point=Point(x=address.latitude, y=address.longitude)
    )

    seed = random.randint(1, 5)
    for i in range(seed):
        relation = random.choice([son, daughter])
        name = get_random_name('male') if relation == son else get_random_name('female')

        today = datetime.datetime.today()
        date = random_date("1997-1-1", "2012-12-31", random.random())
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')

        age = today.year - date_obj.year - ((today.month, today.day) < (date_obj.month, date_obj.day))

        if age > 20:
            address = get_random_address()

        FamillieList.objects.create(
            name=name,
            surname=surname,
            relation=relation,
            date=date,
            address=address,
            point=Point(x=address.latitude, y=address.longitude)
        )


def get_random_address():
    locator = Nominatim(user_agent='geoapp')

    with open('famillies/data/streets.txt', 'r') as reader:
        items = reader.read().split('\n')
        street = random.choice(items)

        building = random.randint(1, 200)
        address = f'{building}, {street} Oblast'

        location = locator.geocode(address)

        if location is None or location.raw['class'] != 'building':
            return get_random_address()

        return location


def get_random_name(gender):
    if gender == 'female':
        with open('famillies/data/female_names.txt', 'r') as reader:
            items = reader.read().split('\n')
            return random.choice(items)
    else:
        with open('famillies/data/male_names.txt', 'r') as reader:
            items = reader.read().split('\n')
            return random.choice(items)


# Date format
def str_time_prop(start, end, format, prop):

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)


# Search field check
def field_is_valid(param):
    return param != '' and param is not None