import ast

from django.core.management.base import BaseCommand, CommandError
from ...models import Draft, Application2018

class Command(BaseCommand):
    help = 'Prints drafts to STDOUT. Usage: python3 manage.py print_drafts > drafts_export.tsv'

    def handle(self, *args, **options):

        # introspection: fields from Application object
        virtual_fields = []
        for f in Application2018._meta.get_fields():
            virtual_fields.append(f.name)
        # make sure that fields from multiwidgets are listed explicitly
        # #todo -- #annualcheck -- check these fields if they are in sync with Application2018
        virtual_fields.remove('gender')
        virtual_fields.extend(('gender_0', 'gender_1'))
        virtual_fields.remove('ethnicity')
        virtual_fields.extend(('ethnicity_0', 'ethnicity_1'))

        # introspection: fields from Draft object
        draft_fields = []
        for f in Draft._meta.get_fields():
            if f.name != 'data':
                draft_fields.append(f.name)

        drafts = Draft.objects.all()

        # print first line with field names
        for field in draft_fields:
            print('draft_' + field + '\t', end='')
        for field in virtual_fields:
            print('virtualfield_' + field + '\t', end='')
        print('')

        # now print values
        for draft in drafts:
            for field in draft_fields:
                # value=str(Draft._meta.get_field(field))
                value=str(getattr(draft, field))
                value=value.replace('\t','    ')
                print(value + '\t', end='')
            data=ast.literal_eval(draft.data)
            for field in virtual_fields:
                value=str(data.get(field, "['*NONEXISTENT*']"))
                value=value.replace('\t','    ')
                print(value + '\t', end='')
            print('')
