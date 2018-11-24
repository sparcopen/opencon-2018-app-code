import csv

from django.core.management.base import BaseCommand, CommandError
from ...models import User


class Command(BaseCommand):
    help = 'Add users to database from /data/user_list.txt'

    def handle(self, *args, **options):
        with open('data/user_list.txt') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            header=next(reader, None)
            # print('Deleting old users...')
            # User.objects.all().delete()
            for row in reader:
                email=row[0]
                first_name=row[1]
                last_name=row[2]
                nick=row[3]
                # DO NOT use "bool", e.g. is_round_0_reviewer=bool(row[4]) -- reason: non-zero-length strings of any value (even if it's "0") are truthy, so bool('0') is True -- solution: instead of "bool(row[4])" simply use "row[4]"
                is_round_0_reviewer=row[4]
                is_round_1_reviewer=row[5]
                is_round_2_reviewer=row[6]
                try:
                    user, created = User.objects.get_or_create(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        nick=nick,
                        is_round_0_reviewer=is_round_0_reviewer,
                        is_round_1_reviewer=is_round_1_reviewer,
                        is_round_2_reviewer=is_round_2_reviewer,
                    )
                    if created:
                        user.save()
                except:
                    print('Failed to import ' + email)
            print('Import of users complete!')
