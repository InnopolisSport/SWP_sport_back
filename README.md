# [SWP] SportComplex service

TODO: change the database

## Requirements:
* Python3
* Docker

## How to start coding
1. Clone the repository
1. Go to repo folder
1. `pip3 install -r ./backend/requirements.txt`
1. Mark `./backend/app` as a Source root
1. To start server 
    1. From repo folder: `docker-compose up -f ./compose/docker-compose.yml`
    1. From `/backend/app`: `docker-compose up -f ../../compose/docker-compose.yml`

Server supports auto-reload on code change

Swagger documentation is at `localhost:<port>/docs`

Redoc documentation is at `localhost:<port>/redoc`
```
.
├── alembic - migration manager
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions - migration folder
├── alembic.ini
└── app
    ├── api - folder for apis
    │   ├── api_v1 - an API
    │   │   ├── api.py - main router for an API
    │   │   ├── endpoints - routers for a particular API group
    │   │   │   ├── __init__.py
    │   │   │   ├── items.py
    │   │   │   ├── login.py
    │   │   │   ├── ping.py
    │   │   │   └── users.py
    │   │   └── __init__.py
    │   ├── __init__.py
    │   └── utils
    │       ├── db.py - common db functional for API
    │       ├── __init__.py
    │       └── security.py - common security functional for API
    ├── backend_pre_start.py - Waiting for a DB to start
    ├── core - core functionality + config
    │   ├── config.py
    │   ├── __init__.py
    │   ├── jwt.py
    │   └── security.py
    ├── crud - CRUD operations on db_models
    │   ├── __init__.py
    │   ├── item.py
    │   └── user.py
    ├── db - classes for alembic
    │   ├── base_class.py
    │   ├── base.py
    │   ├── init_db.py
    │   ├── __init__.py
    │   └── session.py
    ├── db_models - SQL alchemy models
    │   ├── __init__.py
    │   ├── item.py
    │   └── user.py
    ├── initial_data.py -- insert some initial data in DB
    ├── __init__.py
    ├── main.py
    └── models -- Pydantic models
```
