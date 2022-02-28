#!/bin/bash
# name of the django application
NAME="styletransferapp"
# django project dir
DJANGODIR=styletransferapp
# socket
SOCKFILE=run/gunicorn.sock
# the user to run as
USER=root
# num or gunicorn workers
NUM_WORKERS=3
# django settings file
DJANGO_SETTINGS_MODULE=styletransferapp.settings
# wsgi module
DJANGO_WSGI_MODULE=styletransferapp.wsgi

echo "Starting $NAME as `whoami`"
echo "Current config:"
echo "Django app name: $NAME"
echo "Djangodir: $DJANGODIR"
echo "Socket file: $SOCKFILE"
echo "User: $USER"
echo "Number of workers: $NUM_WORKERS"
echo "Django settings module: $DJANGO_SETTINGS_MODULE"
echo "Django wsgi module: DJANGO_WSGI_MODULE"

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE


gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file=-