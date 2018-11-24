from django.core.management.base import BaseCommand, CommandError
from ...models import Institution


class Command(BaseCommand):
    help = 'Add countries to database from /data/institution_list.txt'

    def handle(self, *args, **options):
        with open('data/institution_list.txt') as file:
            for row in file.readlines():
                institution, created = Institution.objects.get_or_create(name=row, show=True)
                if created:
                    institution.save()
