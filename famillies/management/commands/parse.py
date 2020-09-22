from django.core.management.base import BaseCommand
from famillies.models import Surname


class Command(BaseCommand):
    help = 'Fill database table from txt'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help=u'path to txt file')

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'r') as reader:
            for i in reader.readlines():
                Surname.objects.create(surname=i.replace('\n', ''))
