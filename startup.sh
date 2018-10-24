#!/bin/sh

# have to set timeout high enough to prevent worker timeouts
exec gunicorn -w 4 --bind 0.0.0.0:5000 -t 9000 wsgi
