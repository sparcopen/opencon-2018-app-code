from django.core.management.base import BaseCommand, CommandError
from ...models import Airport


class Command(BaseCommand):
    help = 'Add airports to database from /data/airport_list.txt'

    # #todo -- in the future, parse CSV properly -- e.g. if a field contains "Doncaster, Sheffield" (comma inside value), the import will crash (this offending value has been renamed)

    def handle(self, *args, **options):
        index = 0
        with open('data/airport_blacklist.txt') as file:
            filecontent = file.read()
            blacklist = [x.strip() for x in filecontent.strip().splitlines()
                        if not x.strip().startswith('#') and len(x.strip())==3]
        with open('data/airport_list.txt') as file:
            print('Deleting old airports...')
            Airport.objects.all().delete()
            for row in file.readlines():
                data = row.split(',')
                airport_name, city, country, iata_code = (data[1].strip('"'),
                        data[2].strip('"'), data[3].strip('"'), data[4].strip('"'))
                name = city + ' (' + airport_name + '), ' + country
                if iata_code and iata_code not in blacklist:
                    airport = Airport.objects.create(iata_code=iata_code, name=name)
                    airport.save()

                    if index%100 == 0:
                        print('Importing airport: {}'.format(index))
                    index+= 1

            # Finally, add "Other" option
            airport = Airport.objects.create(iata_code='---', name='Other airport')
            airport.save()
