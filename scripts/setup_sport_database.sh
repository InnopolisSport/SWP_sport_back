#!/bin/bash

# before running make sure there no docker volumes (use docker volume prune)

# pass path to the backup file as command-line argument
# sh scripts/setup_sport_database.sh ~/Desktop/sport_16_12_2021_at_04_00.sql

# load backup into the database container
docker-compose -f ./compose/docker-compose.yml down
docker-compose -f ./compose/docker-compose.yml up -d db

docker cp $1 compose_db_1:/database_backup.sql
docker exec compose_db_1 psql -U user -f database_backup.sql postgres
docker exec compose_db_1 rm database_backup.sql

docker-compose -f ./compose/docker-compose.yml down
docker-compose -f ./compose/docker-compose.yml up -d

# save the latest applied sport migration
SPORT_STATE=$(docker exec compose_adminpanel_1 python manage.py showmigrations sport | grep "[X]" | tail -n 1 | cut -c 6-9)

# purge inconsistent migration history and apply migrations appropriately
docker exec compose_db_1 psql -U user -d sport_database -c "DELETE FROM django_migrations"

docker exec compose_adminpanel_1 bash -c "python manage.py makemigrations &&\
python manage.py migrate --fake contenttypes &&\
python manage.py migrate --fake auth 0011 &&\
python manage.py migrate auth 0012 &&\
python manage.py migrate --fake auth &&\
python manage.py migrate --fake accounts &&\
python manage.py migrate --fake admin &&\
python manage.py migrate --fake sessions &&\
python manage.py migrate --fake sites &&\
python manage.py migrate --fake sport $SPORT_STATE &&\
python manage.py migrate"