#!/bin/sh
source venv/bin/activate
flask db upgrade
flask translate compile
exec gunicorn -b :80 --access-logfile - --error-logfile - microblog:app