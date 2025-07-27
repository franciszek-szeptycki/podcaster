#!/bin/bash

set -e

cd /home/podcaster

source ./venv/bin/activate

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput
