#!/bin/sh
python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn config.wsgi --workers 4 --bind=0.0.0.0:5000 --timeout 3600 --chdir=/app
# 2017-04-27`02:14:07 -- added "timeout" for long-running queries -- remember to also update #nginx.conf
