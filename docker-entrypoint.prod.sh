#!/usr/bin/env bash

#pip install -r requirements.txt
python manage.py collectstatic --no-input
# python manage.py compilemessages -l ne -l en
python manage.py migrate --no-input
uwsgi --ini covid.ini