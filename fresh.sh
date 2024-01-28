#!/bin/bash

rm db_dev.sqlite3

# Run makemigrations and migrate
python manage.py makemigrations --settings=settings.development
python manage.py migrate --settings=settings.development

# create superuser
python manage.py create_root_user --settings=settings.development

# Run the custom management commands to create fake data
python manage.py create_fake_questions 8 --settings=settings.development
python manage.py create_fake_weather 100 --settings=settings.development

# create fake rescuetimes, for all the weather dates
python manage.py create_fake_rescuetime --settings=settings.development

# create fake answers to all the questions, for all the weather dates
python manage.py create_fake_answers --settings=settings.development

# start the server
python manage.py runserver --settings=settings.development
