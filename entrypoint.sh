#!/bin/bash
# entrypoint.sh

set -e

# Esperar a que MySQL esté listo
echo "Waiting for MySQL at db:3306..."

while ! mysqladmin ping -h"db" -u"alkosto_user" -p"alkosto_password" --silent; do
    echo "MySQL is unavailable - sleeping"
    sleep 2
done

echo "MySQL is up - proceeding with application startup"

# Colectar archivos estáticos
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate

# Ejecutar el comando principal (Gunicorn)
exec "$@"