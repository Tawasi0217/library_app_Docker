#!/bin/sh
set -eu

python init_db.py
exec gunicorn --bind 0.0.0.0:5000 --workers "${GUNICORN_WORKERS:-2}" wsgi:app
