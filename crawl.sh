#!/usr/bin/env bash

while :
do
    pipenv run python manage.py crawl_vehicles
    sleep 300
done
