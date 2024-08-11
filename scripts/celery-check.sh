#!/bin/sh

set -o errexit
set -o nounset

celery -A finance_api.tasks status || exit 1