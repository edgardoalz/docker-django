#!/bin/sh

PID_FILE=${PID_FILE:-celery_worker.pid}

set -o errexit
set -o nounset

rm -f "./${PID_FILE}"
celery -A finance_api.tasks worker -l INFO --pidfile="${PID_FILE}"