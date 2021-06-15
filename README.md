# [SWP] SportComplex service

![Tests](https://github.com/WinnerOK/SWP_sport_back/workflows/Tests/badge.svg)
![Production deploy](https://github.com/WinnerOK/SWP_sport_back/workflows/Production%20deploy/badge.svg?branch=master)

## Requirements:
* Python3
* Docker

## Environment Variables
See `compose/example.env` for reference.

The project require a file `compose/.env` to contain 
following environment variables:

* `POSTGRES_USER`- Username for the db
* `POSTGRES_PASSWORD`- database password 
* `POSTGRES_DB` - database name
* `POSTGRES_SERVER` - database hostname (`db` - by default)
* `GRAFANA_DB_USER` - username for database user for grafana (will be created if not exists)
* `GRAFANA_DB_PASSWORD` - password for database grafana user
* `GF_SECURITY_ADMIN_PASSWORD` - admin password for Grafana Dashboard
* `SECRET_KEY` - a secret key for token verifications
* `PROJECT_NAME`- project title
* `SCHEMA` - schema of a web page (prefer `https`)
* `HOSTNAME` - hostname of a web page e.g: `example.com`
* `PORT` - port over which web page is served
* `PYTHON_VERSION` - which python version is to be used (specify exact version)
* `DEBUG`- boolean flag for DEBUG mode ( `true` enables fake login and Django debug)
* `oauth_appID` - application ID for oauth
* `oauth_shared_secret` - application secret for ouath
* `oauth_authorization_baseURL`- an URL for user auth
* `oauth_get_infoURL`- tokeninfo URL
* `oauth_tokenURL`- an URL to obtain token 
* `oauth_end_session_endpoint`- end oauth session endpoint


## How to start coding
1. Clone the repository
1. Go to repo folder
1. `pip3 install -r ./adminpage/requirements.txt`
1. To start server 
    1. Rename file: `example.env` to `.env`
    1. From repo folder: `docker-compose -f ./compose/docker-compose.yml up`
1. To create superuser and make migrations
    1. `docker exec -it compose_adminpanel_1 sh`
    1. `python manage.py makemigrations`
    1. `python manage.py migrate`
    1. `python manage.py createsuperuser`

Server supports auto-reload on code change in debug mode

Documentation for `api` module:
* Swagger is at `/api/swagger`
* Redoc is at `/api/redoc`
```
.
├── adminpage - Django project
│   ├── adminpage - main django app
│   │   ├── settings.py
│   │   ├── swagger.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api
│   │   ├── crud - directory with database queries
│   │   ├── fixtures - database tools for testing
│   │   ├── serializers - DRF serializers
│   │   ├── tests
│   │   │   ├── api - endpoints tests
│   │   │   └── crud - database queries tests
│   │   └── views - api endpoints
│   ├── sport
│   │   ├── admin - django adminpage classes
│   │   ├── dumps - database dumps for tests
│   │   ├── migrations - django database migrations
│   │   ├── models - django database models
│   │   ├── signals - django ORM signal handlers
│   │   ├── static - static files for app (css, fonts, images, js)
│   │   │   └── sport
│   │   │       ├── css
│   │   │       ├── fonts
│   │   │       ├── images
│   │   │       └── js
│   │   ├── templates - django templates for app pages
│   │   └── views - app pages url handlers
├── compose - compose for the project
│   └── docker-compose.yml
├── nginx - load balancer and proxy
│   ├── access.d
│   ├── conf - configuration folder
│   ├── Dockerfile
│   └── logs - log folder
├── Dockerfile.db - Dockerfile for db image
└── README.md
```
