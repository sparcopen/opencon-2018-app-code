import csv
import json
import uuid

from django.core.management.base import BaseCommand, CommandError
from ...models import Draft


class Command(BaseCommand):
    help = 'Add drafts from /data/draft_list.txt'

    def handle(self, *args, **options):
        with open('data/draft_list.txt') as file:
            Draft.objects.all().delete()
            reader = csv.reader(file, delimiter=',', quotechar='"')
            header=next(reader, None)
            for row in reader:
                email=row[0]
                data={}
                for i, column in enumerate(row):
                    if row[i]:
                        data[header[i]] = [row[i]]
                data = json.dumps(data) # reason: convert from single-quoted to double-quoted strings
                try:
                    draft, created = Draft.objects.get_or_create(email=email, data=data)
                    # no need to specify 'uuid=str(uuid.uuid4().hex)', 'created at', 'updated at'
                    # also: no need to specify csrfmiddlewaretoken in the data
                    if created:
                        draft.save()
                except:
                    print('Failed to import ' + email)
