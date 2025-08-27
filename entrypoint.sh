#!/bin/bash
# entrypoint.sh

set -e

# Función para esperar a que MySQL esté listo
wait_for_mysql() {
    echo "Waiting for MySQL at db:3306..."
    
    # Usar netcat para verificar que el puerto esté abierto
    while ! nc -z db 3306; do
        echo "MySQL is unavailable - sleeping for 3 seconds"
        sleep 3
    done
    
    echo "MySQL port is open, waiting for service to be ready..."
    
    # Ahora verificar que MySQL esté completamente listo
    while ! mysqladmin ping -h"db" -u"${MYSQL_USER:-alkosto_user}" -p"${MYSQL_PASSWORD:-alkosto_password}" --silent; do
        echo "MySQL service not ready - sleeping for 2 seconds"
        sleep 2
    done
}

# Esperar a que MySQL esté disponible
wait_for_mysql

echo "MySQL is up - proceeding with application startup"

# Crear directorios necesarios
mkdir -p /app/staticfiles

# Colectar archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Aplicar migraciones
echo "Applying database migrations..."
python manage.py migrate --run-syncdb

echo "Starting application..."
# Ejecutar el comando principal (Gunicorn)
exec "$@"