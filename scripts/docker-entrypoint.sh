#!/bin/sh

set -o errexit
set -o nounset

mysql_ready() {
python << END
import sys

from MySQLdb import _mysql

try:
    _mysql.connect(
        database="${SQL_DATABASE}",
        user="${SQL_USER}",
        password="${SQL_PASSWORD}",
        host="${SQL_HOST}",
        port="${SQL_PORT}",
    )
except _mysql.MySQLError:
    sys.exit(-1)
sys.exit(0)

END
}
# until mysql_ready; do
#   >&2 echo 'Waiting for MySQL to become available...'
#   sleep 1
# done
# >&2 echo 'MySQL is available'

exec "$@"