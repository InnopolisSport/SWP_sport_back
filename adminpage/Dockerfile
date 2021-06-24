ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY ./requirements.txt /src/
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r /src/requirements.txt
COPY . /src
