#!/bin/sh

python manage.py runfcgi method=threaded host=127.0.0.1 port=3034 daemonize=false
