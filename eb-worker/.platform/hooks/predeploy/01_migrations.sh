#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/staging

python manage.py collectstatic --noinput
ython manage.py migrate