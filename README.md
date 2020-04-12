# [SWP] SportComplex service

## Requirements:
* Python3
* Docker

## Environment Variables
The project require a file `compose/.env` to contain 
following environment variables:

* `POSTGRES_USER`- Username for the db
* `POSTGRES_PASSWORD`- database password 
* `POSTGRES_DB` - database name
* `POSTGRES_SERVER` - database hostname (`db` - by default)
* `SECRET_KEY` - a secret key for token verifications
* `PROJECT_NAME`- project title
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
├── adminpage - Adminpage django app.
│   ├── adminpage
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── constraints.sql - Constraints that must be present at the db
│   ├── Dockerfile
│   ├── __init__.py
│   ├── manage.py
│   ├── requirements.txt
│   └── sport
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── migrations - auto-generated migrations
│       ├── models - SQL Alchemy db models
│       ├── tests.py
│       └── views.py
├── backend - FAST API app
│   ├── app
│   │   ├── app
│   │   │   ├── api
│   │   │   │   ├── api_v1
│   │   │   │   │   ├── api.py
│   │   │   │   │   ├── endpoints - folder for API endpoints
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── utils - folder for API utilities
│   │   │   ├── backend_pre_start.py
│   │   │   ├── core - Core server functionality
│   │   │   │   ├── config.py - configuration
│   │   │   │   ├── __init__.py
│   │   │   │   ├── jwt.py - token generation
│   │   │   │   └── security.py - user verification
│   │   │   ├── db - folder for CRUD
│   │   │   ├── __init__.py
│   │   │   ├── main.py - sever initialization
│   │   │   ├── models - folder for pydantic models used in the code
│   │   │   ├── backend_pre_start.py - code to be executed before the server run.
│   │   │   ├── pages - code connected to page render
│   │   │   │   ├── endpoints - endpoints for pages
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pages.py
│   │   │   │   └── utils - utils for page rendering
│   │   │   ├── static - folder for all static files
│   │   │   ├── tasks.py - background tasks
│   │   │   ├── templates - jinja2 templates
│   │   │   └── tests - folder for pytest tests
│   │   ├── prestart.sh
│   │   └── requirements.txt
│   ├── Dockerfile
│   └── Dockerfile.db
├── compose - compose for the project
│   └── docker-compose.yml
├── nginx - load balancer and proxy
│   ├── access.d
│   ├── conf - configuration folder
│   ├── Dockerfile
│   └── logs - log folder
└── README.md

```
