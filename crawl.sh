#!/usr/bin/env bash

while :
do
    pipenv run python manage.py crawl_vehicles
    pipenv run python manage.py estimate_trips
    sleep 150
done
