#!/bin/bash
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for MySQL at $host..."

while ! mysqladmin ping -h"$host" -u"alkosto_user" -p"alkosto_password" --silent; do
    echo "MySQL is unavailable - sleeping"
    sleep 2
done

echo "MySQL is up - executing command"
exec $cmd