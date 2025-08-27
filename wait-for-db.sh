#!/bin/bash
# wait-for-db.sh

host="$1"
shift
cmd="$@"

echo "Waiting for MySQL at $host:3306..."

while ! nc -z $host 3306; do
    echo "MySQL is unavailable - sleeping"
    sleep 2
done

echo "MySQL is up - executing command"
exec $cmd