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
