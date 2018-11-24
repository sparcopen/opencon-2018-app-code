#!/usr/bin/env bash
rm db.sqlite3
rm -R application/migrations
rm -R rating/migrations
./manage.py makemigrations application
./manage.py makemigrations rating
./manage.py migrate
./manage.py add_countries
./manage.py add_institutions
./manage.py add_organizations
./manage.py createsuperuser --user admin --email admin@example.com
