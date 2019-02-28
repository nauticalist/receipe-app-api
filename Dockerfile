FROM python:3.7.2-alpine
MAINTAINER Seanapse Oü

ENV PYTHONUNBUFFERED 1
# Install necessary requirements
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# Copy files to server
RUN mkdir /app
WORKDIR /app
COPY ./app /app
# Create user to run the app only
RUN adduser -D django
RUN chown -R django:django /app
RUN chmod -R 777 /app
USER django


