#!/bin/sh

set -o errexit
set -o nounset
mkdir -p /app/staticfiles \
    && chown -R app:app /app/staticfiles \
    && chmod -R 755 /app/staticfiles
python manage.py collectstatic --noinput
chown -R app:app /app/staticfiles
python manage.py migrate --noinput
gunicorn finance_api.wsgi:application --bind "0.0.0.0:$PORT"