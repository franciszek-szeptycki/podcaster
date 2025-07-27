#!/bin/bash

set -e

# cd /home/podcaster

# source ./venv/bin/activate

# pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

gunicorn podcaster.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
