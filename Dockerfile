FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin gettext

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT /code/docker-entrypoint.local.sh
