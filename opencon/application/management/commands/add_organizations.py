from django.core.management.base import BaseCommand, CommandError
from ...models import Organization


class Command(BaseCommand):
    help = 'Add countries to database from /data/organization_list.txt'

    def handle(self, *args, **options):
        with open('data/organization_list.txt') as file:
            for row in file.readlines():
                organization, created = Organization.objects.get_or_create(name=row, show=True)
                if created:
                    organization.save()
