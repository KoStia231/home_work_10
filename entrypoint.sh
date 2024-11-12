#!/bin/bash

echo "Applying migrations..."
python manage.py migrate

echo "Running load db.json"
python manage.py loaddata db.json

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000