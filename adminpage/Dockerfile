
#FROM python:${PYTHON_DOCKER_VERSION}
#ENV PYTHONUNBUFFERED 1
#RUN mkdir /src
#WORKDIR /src
#COPY ./requirements.txt /src/
#RUN pip install -r /src/requirements.txt
#COPY . /src

# -------------------------------------------------------------

FROM python:3.7-alpine as base
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt requirements.txt ./
#RUN apk add --update --no-cache --virtual .build-deps \
#    build-base \
#    postgresql-dev \
#    libffi-dev \
#    python3-dev \
#    libffi-dev \
#    jpeg-dev \
#    zlib-dev \
#    musl-dev \
#    libpq \
#    && pip install --no-cache-dir -r requirements.txt \
#    && find /usr/local \
#        \( -type d -a -name test -o -name tests \) \
#        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
#        -exec rm -rf '{}' +

RUN apk add --update --no-cache --virtual .build-deps \
    build-base \
    postgresql-dev \
    libffi-dev \
    python3-dev \
    libffi-dev \
    jpeg-dev \
    zlib-dev \
    musl-dev \
    libpq
RUN pip install --no-cache-dir -r requirements.txt
RUN find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' +

# Now multistage builds
FROM python:3.7-alpine
RUN apk add --update --no-cache libpq libjpeg-turbo bash

COPY --from=base /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

WORKDIR /src

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /src:$PYTHONPATH
#EXPOSE 8080

COPY . /src/

