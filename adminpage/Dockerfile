ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r /src/requirements.txt