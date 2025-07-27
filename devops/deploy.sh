#!/bin/bash

set -e

cd /home/podcaster

source ./devops/configure_prod.sh

git pull origin main

source ./venv/bin/activate

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

systemctl restart podcaster.service
