from django.core.management.base import BaseCommand, CommandError
from ...models import Country


class Command(BaseCommand):
    help = 'Add countries to database from /data/country_list.txt'

    def handle(self, *args, **options):
        with open('data/country_list.txt') as file:
            Country.objects.all().delete()
            for row in file.readlines():
                country = Country.objects.create(name=row)
                country.save()
