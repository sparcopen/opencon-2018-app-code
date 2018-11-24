from django.core.management.base import BaseCommand, CommandError
from ...models import Application2018
import sys


class Command(BaseCommand):
    help = 'Recalculate ratings for applications'

    def handle(self, *args, **options):
        applications = Application2018.objects.all()
        app_count = applications.count()

        # # for testing: recalculate a single application (faster than recalculating all)
        # myapp = applications.filter(email__icontains='...').first()
        # myapp.save()
        # return

        for i, application in enumerate(applications):
            application.save()
            if i % 20 == 0:
                sys.stdout.write('\rRecalculated: {0:.2f}%'.format(i/app_count*100))

        print('\nRecalculation done!')
