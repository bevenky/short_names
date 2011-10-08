#!/bin/bash

VENV=/usr/src/python_env/bin
PROJECT_PATH=/usr/src/short_names

LOGFILE=/var/log/gunicorn_sn.log
LOGLEVEL=debug
NUM_WORKERS=1

URL=184.75.242.142

PID=/var/run/gunicorn_sn.pid

set -e

# user/group to run as
USER=root
GROUP=root

rm -f $PID

cd $PROJECT_PATH
source $VENV/activate
exec $VENV/gunicorn -b $URL -w $NUM_WORKERS --user=$USER --group=$GROUP --pid=$PID --log-level=$LOGLEVEL --log-file=$LOGFILE  2>>$LOGFILE short_names:app
