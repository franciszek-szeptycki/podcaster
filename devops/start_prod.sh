#!/bin/bash

GUNICORN=`/home/podcaster/venv/bin/gunicorn`
PYTHON=`/home/podcaster/venv/bin/python`

$PYTHON manage.py collectstatic --noinput
$PYTHON manage.py migrate --noinput

$GUNICORN podcaster.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
