FROM python:3.7.4-alpine
MAINTAINER Seanapse Oü

ENV PYTHONUNBUFFERED 1
# Install necessary requirements
COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

# Copy files to server
RUN mkdir /app
WORKDIR /app
COPY ./app /app
# Create user to run the app only
RUN adduser -D django
RUN chown -R django:django /app
USER django