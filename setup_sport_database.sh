#!/bin/bash

# pass path to the backup file as command-line argument
# sh setup_sport_database.sh ~/Desktop/sport_16_12_2021_at_04_00.sql

# load backup into the database container
sudo docker-compose -f ./compose/docker-compose.yml stop
sudo docker start compose_db_1

sudo docker cp $1 compose_db_1:/database_backup.sql
sudo docker exec compose_db_1 psql -U user -f database_backup.sql postgres
sudo docker exec compose_db_1 rm database_backup.sql

sudo docker-compose -f ./compose/docker-compose.yml start

# save the latest applied sport migration
SPORT_STATE=$(sudo docker exec compose_adminpanel_1 python manage.py showmigrations sport | grep "[X]" | tail -n 1 | cut -c 6-9)

# purge inconsistent migration history and apply migrations appropriately
sudo docker exec compose_db_1 psql -U user -d sport_database -c "DELETE FROM django_migrations"

sudo docker exec compose_adminpanel_1 python manage.py migrate --fake contenttypes

sudo docker exec compose_adminpanel_1 python manage.py migrate --fake auth 0011
sudo docker exec compose_adminpanel_1 python manage.py migrate auth 0012
sudo docker exec compose_adminpanel_1 python manage.py migrate --fake auth

sudo docker exec compose_adminpanel_1 python manage.py migrate --fake accounts
sudo docker exec compose_adminpanel_1 python manage.py migrate --fake admin
sudo docker exec compose_adminpanel_1 python manage.py migrate --fake sessions
sudo docker exec compose_adminpanel_1 python manage.py migrate --fake sites

sudo docker exec compose_adminpanel_1 python manage.py migrate --fake sport $SPORT_STATE
sudo docker exec compose_adminpanel_1 python manage.py makemigrations
sudo docker exec compose_adminpanel_1 python manage.py migrate sport