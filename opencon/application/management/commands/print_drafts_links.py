import ast

from django.core.management.base import BaseCommand, CommandError
from ...models import Draft

class Command(BaseCommand):
    help = 'Prints links to drafts to STDOUT. Usage: python3 manage.py print_drafts_links > drafts_links.tsv'

    def handle(self, *args, **options):
        drafts = Draft.objects.all()
        for draft in drafts:
            # #todo -- #annualcheck -- check the URL (openconXXXX.org)
            print(str(draft.email) + '\t' + 'https://apply.opencon2018.org/saved/' + str(draft.uuid))
