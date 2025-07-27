#!/bin/bash

set -e

GUNICORN=`/home/podcaster/venv/bin/gunicorn`
PYTHON=`/home/podcaster/venv/bin/python`
WORKDIR=/home/podcaster

cd $WORKDIR

$WORKDIR/venv/bin/pip3 install -r requirements.txt

$PYTHON manage.py collectstatic --noinput
$PYTHON manage.py migrate --noinput
