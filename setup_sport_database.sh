#!/bin/bash

# pass path to the backup file as command-line argument
# sh setup_sport_database.sh ~/Desktop/sport_16_12_2021_at_04_00.sql

# load backup into the database container
docker-compose -f ./compose/docker-compose.yml stop
docker start compose_db_1

docker cp $1 compose_db_1:/database_backup.sql
docker exec compose_db_1 psql -U user -f database_backup.sql postgres
docker exec compose_db_1 rm database_backup.sql

docker-compose -f ./compose/docker-compose.yml start

# save the latest applied sport migration
SPORT_STATE=$(docker exec compose_adminpanel_1 python manage.py showmigrations sport | grep "[X]" | tail -n 1 | cut -c 6-9)

# purge inconsistent migration history and apply migrations appropriately
docker exec compose_db_1 psql -U user -d sport_database -c "DELETE FROM django_migrations"

docker exec compose_adminpanel_1 python manage.py migrate --fake contenttypes

docker exec compose_adminpanel_1 python manage.py migrate --fake auth 0011
docker exec compose_adminpanel_1 python manage.py migrate auth 0012
docker exec compose_adminpanel_1 python manage.py migrate --fake auth

docker exec compose_adminpanel_1 python manage.py migrate --fake accounts
docker exec compose_adminpanel_1 python manage.py migrate --fake admin
docker exec compose_adminpanel_1 python manage.py migrate --fake sessions
docker exec compose_adminpanel_1 python manage.py migrate --fake sites

docker exec compose_adminpanel_1 python manage.py migrate --fake sport $SPORT_STATE
docker exec compose_adminpanel_1 python manage.py makemigrations
docker exec compose_adminpanel_1 python manage.py migrate sport