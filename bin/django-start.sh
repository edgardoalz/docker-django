#!/bin/sh

set -o errexit
set -o nounset

gunicorn finance_api.wsgi:application --bind "0.0.0.0:$PORT"